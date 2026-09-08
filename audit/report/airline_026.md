# Audit report — airline_026

| step | agent | module | signal | evidence |
|---|---|---|---|---|
| 4 | planner | D1/tool | {"confidence": 0.615, "p_actual": 0.562, "margin": 0.124} | action distribution: db_agent 0.56, policy_checker 0.44, read_file 0.00 (actual: db_agent) |
| 5 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: user_id=aarav_ahmed_6699 |
| 10 | planner | D1/tool | {"confidence": 0.552, "p_actual": 0.643, "margin": 0.339} | action distribution: policy_checker 0.64, db_agent 0.30, respond_to_user 0.05 (actual: policy_checker) |
| 11 | policy_checker | D3 | {"satisfied": false} | claims without prior tool evidence: reservation_id=M20IZO |
| 18 | db_agent | D1/tool | {"confidence": 0.772, "p_actual": 0.821, "margin": 0.704} | action distribution: search_direct_flight 0.82, calculate 0.12, search_onestop_flight 0.04 (actual: search_direct_flight) |
| 18 | db_agent | D2 | {"s": 0.25, "unsupported": 0.75} | values not found in any prior tool result: HAT268 (JFK to ATL, $136), HAT010 (ATL to MCO, $109), $245, Calculate price difference for upgrading to business class |
| 18 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=245 |
| 20 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=294, money=597, money=303 |
| 21 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 25 | db_agent | D3 | {"checks": ["repeat"], "tool": "get_reservation_details"} | tool get_reservation_details call #16: repeat |
| 25 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 26 | db_agent | D3 | {"checks": ["error"], "tool": "update_reservation_flights"} | tool update_reservation_flights call #17: error |
| 26 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 27 | db_agent | D1/tool | {"confidence": 0.759, "p_actual": 0.394, "margin": 0.211} | action distribution: no_tool 0.60, get_user_details 0.39, transfer_to_human_agents 0.00 (actual: get_user_details) |
| 27 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 28 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 29 | db_agent | D1/tool | {"confidence": 0.687, "p_actual": 0.266, "margin": 0.367} | action distribution: no_tool 0.63, read_file 0.27, write_file 0.10 (actual: read_file) |
| 29 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |
| 30 | db_agent | D3 | {"satisfied": false} | claims without prior tool evidence: money=597 |

## Per-module summary
```
{
 "D1": {
  "n_scored": 28,
  "method": "stepwise"
 },
 "D2": {
  "n_utterances": 17,
  "n_na": 2
 },
 "D3": {
  "tool_calls": 23,
  "utterances": 16,
  "checks": {
   "repeat": 1,
   "error": 1
  }
 },
 "D7": {
  "n_handoffs": 10
 }
}
```

Thresholds (label-free, top 10% per item): `{"percentile": 10, "D1": {"planner": 0.3389318650067048, "subagent": 0.22245623061646203}, "D1_handoff": 0.4560107138530137, "D2": 0.5555555555555556, "D7": 1.0, "D9": 0.9333333333333333}`