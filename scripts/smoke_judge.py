"""Smoke test: confirm the OpenAI-compatible judge backend answers a trivial JSON question."""
import json, sys, time, yaml
from openai import OpenAI

cfg = yaml.safe_load(open("configs/judge.yaml"))
client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
t0 = time.time()
r = client.chat.completions.create(
    model=cfg["model"],
    temperature=cfg["temperature"],
    max_tokens=128,
    messages=[
        {"role": "system", "content": "Answer only with a JSON object."},
        {"role": "user", "content": 'A tool returned an error "HTTP 500" and the agent then reported success to the user. Is this a failure? Reply {"failure": true|false, "type": "<one word>"}'},
    ],
    extra_body={"chat_template_kwargs": {"enable_thinking": cfg["enable_thinking"]}},
)
txt = r.choices[0].message.content
print("latency %.1fs | tokens in/out %d/%d" % (time.time() - t0, r.usage.prompt_tokens, r.usage.completion_tokens))
print(txt)
json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
print("JUDGE SMOKE OK")
