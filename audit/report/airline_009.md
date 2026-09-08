# Audit report — airline_009

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 2 | planner | D7/report->planner | {"fidelity": 0.0, "missing": ["gift_card_and_certificate_balances", "successful"], "altered": []} | db_agent report->planner: missing ['gift_card_and_certificate_balances', 'successful'] altered [] |
| 5 | planner | D1/tool | {"confidence": 0.661, "p_actual": 0.704, "margin": 0.409} | action distribution: no_tool 0.70, respond_to_user 0.30, db_agent 0.00 (actual: no_tool) |

## Per-module summary
```
{
 "D1": {
  "n_scored": 4,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 3,
  "n_na": 3
 },
 "D3": {
  "tool_calls": 2,
  "utterances": 0,
  "checks": {}
 },
 "D7": {
  "n_handoffs": 2
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`