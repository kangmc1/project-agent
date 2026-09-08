"""P1 gate: verify the three vLLM servers and the D1 scoring assumptions.

Checks (see .omc/plans/agent-failure-detection-plan.md P1):
 (a) tool-bound chat call on 18001 returns a tool_call
 (b) the same response carries generated-token logprobs
 (c) /v1/completions prompt_logprobs=1 max_tokens=1 works on 18003
 (d) "<tool_call>" is a single token (id 151657)
 (e) /tokenize (messages+tools+enable_thinking=false) token ids == local apply_chat_template (3 samples)
 (f) 8B server returns parseable JSON for an extraction prompt
 (h) OPENAI_BASE_URL / OPENAI_API_BASE point to the local executor server
 (i) allowed_token_ids=[t] returns t's logprob and it equals the unmasked value
 (j) 18003 log reports GPU KV cache size >= 1.2 x max-model-len
Exit code 0 only if every check passes.  Run: python scripts/check_server.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

try:
    import httpx2 as hx  # openai>=3 ships httpx2
except ImportError:  # pragma: no cover
    import httpx as hx

from transformers import AutoTokenizer

EXEC = "http://localhost:18001/v1"
EXTR = "http://localhost:18002/v1"
SCORE = "http://localhost:18003/v1"
Q32 = os.environ.get("Q32") or next(
    p for p in __import__("glob").glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3-32B/snapshots/*"))
)
TOOL_CALL_ID = 151657
NO_THINK = {"chat_template_kwargs": {"enable_thinking": False}}
RESULTS: dict[str, tuple[bool, str]] = {}


def record(name: str, ok: bool, info: str = "") -> None:
    RESULTS[name] = (ok, info)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")


def wait_ready(base: str, timeout: int = 1500) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = hx.get(base + "/models", timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(10)
    return False


WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather for a city",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
}


def check_ab() -> None:
    body = {
        "model": "qwen32b",
        "messages": [{"role": "user", "content": "What is the weather in Paris? Use the tool."}],
        "tools": [WEATHER_TOOL],
        "tool_choice": "auto",
        "temperature": 0,
        "max_tokens": 128,
        "logprobs": True,
        "top_logprobs": 0,
        **NO_THINK,
    }
    r = hx.post(EXEC + "/chat/completions", json=body, timeout=120)
    ch = r.json()["choices"][0]
    tc = ch["message"].get("tool_calls") or []
    record("a_tool_call", bool(tc) and tc[0]["function"]["name"] == "get_weather", json.dumps(tc)[:120])
    lp = (ch.get("logprobs") or {}).get("content") or []
    record("b_logprobs_on_tool_call", len(lp) > 0, f"n_tokens={len(lp)} first={lp[0]['token'] if lp else None!r}")


def check_c() -> None:
    r = hx.post(
        SCORE + "/completions",
        json={"model": "qwen32b-score", "prompt": "<tool_call>\n{\"name\": \"get_weather\"", "max_tokens": 1,
              "prompt_logprobs": 1, "temperature": 0},
        timeout=120,
    )
    d = r.json()
    pl = d["choices"][0].get("prompt_logprobs")
    record("c_prompt_logprobs", isinstance(pl, list) and len(pl) > 1 and pl[1] is not None, f"len={len(pl) if pl else None}")


def check_d(tok) -> None:
    ids = tok.encode("<tool_call>", add_special_tokens=False)
    record("d_tool_call_single_token", ids == [TOOL_CALL_ID], str(ids))


def check_e(tok) -> None:
    samples = [
        ([{"role": "user", "content": "hi"}], [WEATHER_TOOL]),
        ([{"role": "system", "content": "You are a helpful agent."},
          {"role": "user", "content": "Cancel reservation ZFA04Y"},
          {"role": "assistant", "content": "", "tool_calls": [{"id": "call_1", "type": "function",
             "function": {"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}}]},
          {"role": "tool", "tool_call_id": "call_1", "content": "sunny"}], [WEATHER_TOOL]),
        ([{"role": "user", "content": "Solve 1+1"}], []),
    ]
    all_ok = True
    for i, (msgs, tools) in enumerate(samples):
        body = {"model": "qwen32b", "messages": msgs, "add_generation_prompt": True, **NO_THINK}
        if tools:
            body["tools"] = tools
        r = hx.post("http://localhost:18001/tokenize", json=body, timeout=60)
        server_ids = r.json()["tokens"]
        text = tok.apply_chat_template(msgs, tools=tools or None, add_generation_prompt=True,
                                       tokenize=False, enable_thinking=False)
        local_ids = tok(text, add_special_tokens=False)["input_ids"]
        ok = list(server_ids) == list(local_ids)
        all_ok &= ok
        if not ok:
            print(f"   sample {i}: server={len(server_ids)} local={len(local_ids)}")
            print("   server tail:", tok.decode(server_ids[-40:]))
            print("   local  tail:", tok.decode(local_ids[-40:]))
    record("e_tokenize_equals_local_render", all_ok)


def check_f() -> None:
    body = {"model": "qwen8b", "temperature": 0, "max_tokens": 200, **NO_THINK,
            "messages": [{"role": "user", "content": 'Extract claims as JSON {"claims":[{"entity":..,"attribute":..,"value":..}]} '
                                                    'from: "Reservation ZFA04Y total is $340 and the fee is $50." Output JSON only.'}]}
    r = hx.post(EXTR + "/chat/completions", json=body, timeout=120)
    txt = r.json()["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", txt, re.S)
    ok = False
    try:
        ok = m is not None and "claims" in json.loads(m.group(0))
    except Exception:
        ok = False
    record("f_8b_json_extraction", ok, txt[:100].replace("\n", " "))


def check_h() -> None:
    a, b = os.environ.get("OPENAI_BASE_URL", ""), os.environ.get("OPENAI_API_BASE", "")
    record("h_env_base_urls", a.startswith("http://localhost:18001") and b.startswith("http://localhost:18001"), f"{a} {b}")


def check_i(tok) -> None:
    prompt = "The capital of France is"
    paris = tok.encode(" Paris", add_special_tokens=False)
    assert len(paris) == 1, paris
    t = paris[0]
    masked = hx.post(SCORE + "/completions", json={"model": "qwen32b-score", "prompt": prompt, "max_tokens": 1,
                                                    "logprobs": 1, "temperature": 0, "allowed_token_ids": [t]}, timeout=120).json()
    unmasked = hx.post(SCORE + "/completions", json={"model": "qwen32b-score", "prompt": prompt, "max_tokens": 1,
                                                      "logprobs": 20, "temperature": 0}, timeout=120).json()
    m_lp = masked["choices"][0]["logprobs"]
    m_tok = m_lp["tokens"][0]
    m_val = m_lp["token_logprobs"][0]
    u_top = unmasked["choices"][0]["logprobs"]["top_logprobs"][0]
    u_val = u_top.get(m_tok)
    ok = (m_tok in u_top) and u_val is not None and abs(u_val - m_val) < 1e-3
    record("i_allowed_token_ids_raw_logprob", ok, f"masked={m_tok!r}:{m_val:.4f} unmasked={u_val}")


def check_j() -> None:
    try:
        log = open("logs/vllm32b_score.log", encoding="utf-8", errors="ignore").read()
        m = re.search(r"GPU KV cache size:\s*([\d,]+) tokens", log)
        kv = int(m.group(1).replace(",", "")) if m else -1
        m2 = re.search(r"max_seq_len=(\d+)", log)
        mx = int(m2.group(1)) if m2 else 24576
        record("j_kv_cache_headroom", kv >= 1.2 * mx, f"kv={kv} max_len={mx} ratio={kv / mx if mx else 0:.2f}")
    except Exception as e:  # pragma: no cover
        record("j_kv_cache_headroom", False, repr(e))


def main() -> int:
    for base in (EXEC, EXTR, SCORE):
        print("waiting", base, "...", wait_ready(base))
    tok = AutoTokenizer.from_pretrained(Q32)
    for fn in (check_ab, check_c, lambda: check_d(tok), lambda: check_e(tok), check_f, check_h, lambda: check_i(tok), check_j):
        try:
            fn()
        except Exception as e:
            record(getattr(fn, "__name__", "lambda"), False, repr(e)[:200])
    ok = all(v[0] for v in RESULTS.values())
    json.dump({k: {"pass": v[0], "info": v[1]} for k, v in RESULTS.items()}, open("logs/check_server.json", "w"), indent=2)
    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
