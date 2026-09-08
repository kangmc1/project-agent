"""vLLM (OpenAI-compatible) client: live-pool round robin, disk cache, guided JSON, token counting, usage accounting.

Every call is cached on disk keyed by the full request + sample_idx, so re-runs are free and reproducible.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from openai import OpenAI

DEFAULT_ENDPOINTS = ["http://localhost:18001/v1", "http://localhost:18002/v1",
                     "http://localhost:18003/v1", "http://localhost:18004/v1"]


@dataclass
class Usage:
    calls: int = 0
    cached: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0
    by_tag: dict = field(default_factory=dict)


class LLM:
    def __init__(self, endpoints: list[str] | None = None, model: str | None = None,
                 cache_dir: str | Path = "data/cache", timeout: float = 600.0):
        env_eps = os.environ.get("HC_ENDPOINTS")
        self.endpoints = endpoints or (env_eps.split(",") if env_eps else DEFAULT_ENDPOINTS)
        self.model = model or os.environ.get("HC_MODEL", "qwen3-8b")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self._lock = threading.Lock()
        self._rr = 0
        self._fail = {ep: 0 for ep in self.endpoints}
        self._clients = {ep: OpenAI(base_url=ep, api_key="EMPTY", timeout=timeout, max_retries=0) for ep in self.endpoints}
        self.usage = Usage()
        self._tok_cache: dict[str, int] = {}
        self.live = self.health()

    # ---------- pool ----------
    def health(self) -> list[str]:
        live = []
        for ep in self.endpoints:
            try:
                r = httpx.get(ep.rsplit("/v1", 1)[0] + "/health", timeout=5)
                if r.status_code == 200:
                    live.append(ep)
            except Exception:
                pass
        if not live:
            raise RuntimeError(f"no live vLLM endpoint among {self.endpoints}")
        return live

    def _pick(self) -> str:
        with self._lock:
            if not self.live:
                self.live = self.health()
            ep = self.live[self._rr % len(self.live)]
            self._rr += 1
            return ep

    def _mark(self, ep: str, ok: bool) -> None:
        with self._lock:
            if ok:
                self._fail[ep] = 0
            else:
                self._fail[ep] += 1
                if self._fail[ep] >= 3 and ep in self.live and len(self.live) > 1:
                    self.live.remove(ep)

    # ---------- cache ----------
    def _key(self, payload: dict) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    # ---------- chat ----------
    def chat(self, messages: list[dict], *, temperature: float = 0.0, max_tokens: int = 1024,
             guided_json: dict | None = None, sample_idx: int = 0, thinking: bool = False,
             tag: str = "", stop: list[str] | None = None) -> dict:
        payload = {"model": self.model, "messages": messages, "temperature": temperature,
                   "max_tokens": max_tokens, "guided_json": guided_json, "sample_idx": sample_idx,
                   "thinking": thinking, "stop": stop}
        key = self._key(payload)
        cpath = self.cache_dir / f"{key}.json"
        if cpath.exists():
            out = json.loads(cpath.read_text())
            out["cached"] = True
            self._account(out, tag, cached=True)
            return out
        extra = {"chat_template_kwargs": {"enable_thinking": bool(thinking)}}
        if guided_json is not None:
            extra["guided_json"] = guided_json
        last_err = None
        for attempt in range(4):
            ep = self._pick()
            t0 = time.time()
            try:
                resp = self._clients[ep].chat.completions.create(
                    model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens,
                    seed=sample_idx, stop=stop, extra_body=extra)
                text = resp.choices[0].message.content or ""
                # Qwen3 thinking: strip <think> blocks if present
                if "<think>" in text and "</think>" in text:
                    text = text.split("</think>", 1)[1].lstrip()
                out = {"text": text, "finish": resp.choices[0].finish_reason,
                       "usage": {"prompt": resp.usage.prompt_tokens if resp.usage else 0,
                                 "completion": resp.usage.completion_tokens if resp.usage else 0},
                       "elapsed": time.time() - t0, "endpoint": ep, "cached": False}
                self._mark(ep, True)
                cpath.write_text(json.dumps(out, ensure_ascii=False))
                self._account(out, tag, cached=False)
                return out
            except Exception as e:  # noqa: BLE001
                last_err = e
                self._mark(ep, False)
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"LLM call failed after retries: {last_err}")

    def chat_json(self, messages: list[dict], schema: dict | None = None, **kw) -> tuple[dict | list | None, dict]:
        """Chat expecting JSON. Uses guided decoding when a schema is given; falls back to lenient parsing."""
        out = self.chat(messages, guided_json=schema, **kw)
        obj = parse_json_lenient(out["text"])
        if obj is None and schema is None:
            kw2 = dict(kw)
            kw2["sample_idx"] = kw.get("sample_idx", 0) + 100
            out = self.chat(messages + [{"role": "user", "content": "Return ONLY valid JSON."}], **kw2)
            obj = parse_json_lenient(out["text"])
        out["parsed_ok"] = obj is not None
        return obj, out

    def _account(self, out: dict, tag: str, cached: bool) -> None:
        with self._lock:
            u = self.usage
            u.calls += 1
            u.cached += int(cached)
            u.prompt_tokens += out.get("usage", {}).get("prompt", 0)
            u.completion_tokens += out.get("usage", {}).get("completion", 0)
            u.seconds += 0 if cached else out.get("elapsed", 0)
            t = u.by_tag.setdefault(tag or "untagged", {"calls": 0, "cached": 0, "prompt": 0, "completion": 0})
            t["calls"] += 1
            t["cached"] += int(cached)
            t["prompt"] += out.get("usage", {}).get("prompt", 0)
            t["completion"] += out.get("usage", {}).get("completion", 0)

    # ---------- tokens ----------
    def count_tokens(self, text: str) -> int:
        h = hashlib.sha1(text.encode()).hexdigest()
        if h in self._tok_cache:
            return self._tok_cache[h]
        ep = self._pick()
        base = ep.rsplit("/v1", 1)[0]
        try:
            r = httpx.post(base + "/tokenize", json={"model": self.model, "prompt": text}, timeout=60)
            r.raise_for_status()
            n = int(r.json()["count"])
        except Exception:
            n = max(1, len(text) // 3)
        self._tok_cache[h] = n
        return n


def parse_json_lenient(text: str):
    if text is None:
        return None
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
    t = t.strip()
    try:
        return json.loads(t)
    except Exception:
        pass
    # first balanced {...} or [...]
    for open_c, close_c in (("{", "}"), ("[", "]")):
        i = t.find(open_c)
        if i < 0:
            continue
        depth = 0
        for j in range(i, len(t)):
            if t[j] == open_c:
                depth += 1
            elif t[j] == close_c:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(t[i:j + 1])
                    except Exception:
                        break
    return None
