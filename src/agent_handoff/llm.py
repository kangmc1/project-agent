"""Thin OpenAI-compatible chat client (local vLLM by default) with JSON extraction and usage accounting."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from openai import OpenAI


@dataclass
class Usage:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0

    def add(self, r, dt: float):
        self.calls += 1
        if getattr(r, "usage", None):
            self.prompt_tokens += r.usage.prompt_tokens or 0
            self.completion_tokens += r.usage.completion_tokens or 0
        self.seconds += dt

    def as_dict(self):
        return {"calls": self.calls, "prompt_tokens": self.prompt_tokens, "completion_tokens": self.completion_tokens, "seconds": round(self.seconds, 2)}


class LLM:
    def __init__(self, config: str | Path = "configs/judge.yaml", **overrides):
        cfg = yaml.safe_load(open(config))
        cfg.update(overrides)
        self.cfg = cfg
        self.client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
        self.model = cfg["model"]
        self.usage = Usage()

    def chat(self, system: str, user: str, max_tokens: int | None = None, temperature: float | None = None, thinking: bool | None = None) -> str:
        t0 = time.time()
        r = self.client.chat.completions.create(
            model=self.model,
            temperature=self.cfg["temperature"] if temperature is None else temperature,
            max_tokens=max_tokens or self.cfg["max_tokens"],
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            extra_body={"chat_template_kwargs": {"enable_thinking": self.cfg["enable_thinking"] if thinking is None else thinking}},
        )
        self.usage.add(r, time.time() - t0)
        return r.choices[0].message.content or ""

    def chat_json(self, system: str, user: str, retries: int = 2, **kw) -> dict | list:
        last = ""
        for attempt in range(retries + 1):
            txt = self.chat(system, user, **kw)
            last = txt
            obj = extract_json(txt)
            if obj is not None:
                return obj
            user = user + "\n\nYour previous reply was not valid JSON. Reply with ONLY a single JSON object."
        raise ValueError(f"no JSON after {retries+1} attempts: {last[:300]}")


def extract_json(txt: str):
    txt = re.sub(r"<think>.*?</think>", "", txt, flags=re.S).strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", txt, re.S)
    if m:
        txt = m.group(1)
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = txt.find(opener), txt.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(txt[i : j + 1])
            except json.JSONDecodeError:
                continue
    return None
