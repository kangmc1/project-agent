# System stability report (label-free)

Flag thresholds = top 10% of each item's own distribution (per role). `success_rate*` uses ground truth and is shown for reference only.

## aime — 31 runs, success_rate* = 0.25806451612903225

### Agents

| agent | decisions | mean conf | low-conf ratio | handoff-layer low | ungrounded-arg ratio | tool calls | error | empty | repeat | schema | ignored |
|---|---|---|---|---|---|---|---|---|---|---|---|
| planner | 127 | 0.93 | 0.11 | 0.11 | 0.01 | 95 | 0.02 | 0.00 | 0.01 | 0.00 | 0.02 |
| solver | 180 | 0.97 | 0.12 | - | - | 137 | 0.18 | 0.00 | 0.63 | 0.00 | 0.00 |
| verifier | 83 | 0.97 | 0.07 | - | - | 54 | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 |

### Handoff edges

| edge | n | mean fidelity | low(<0.8) ratio | top missing | top altered |
|---|---|---|---|---|---|
| solver:instruction->premise | 43 | 0.75 | 0.42 | [('n', 4), ('m', 3), ('2', 2)] | [('final_answer', 3), ('distance_miles', 2), ('problem_statement', 2)] |
| solver:report->planner | 43 | 0.31 | 0.83 | [('1', 5), ('s', 4), ('r', 4)] | [('final_answer', 11), ('m_plus_n', 1)] |
| verifier:instruction->premise | 29 | 0.80 | 0.39 | [('m', 4), ('n', 3), ('2', 2)] | [('m', 2), ('n', 2), ('final_answer', 2)] |
| verifier:report->planner | 29 | 0.52 | 0.61 | [('0', 5), ('20', 2), ('2', 2)] | [('final_answer', 1)] |

### Hotspots (top 5)

- solver: claim numeric without tool evidence — 324
- verifier: claim numeric without tool evidence — 113
- solver: run_python repeat — 86
- verifier: run_python repeat — 27
- solver: run_python error — 25

### Confidence by decision index

{
 "decisions 0-4": 0.9730679461869883,
 "decisions 5-9": 0.9284856804591334,
 "decisions 10-14": 0.933150825093611,
 "decisions 15-19": 0.9636136586359234,
 "decisions 20-24": 0.9728598784357543,
 "decisions 25+": 0.9715400044569166
}

## airline — 31 runs, success_rate* = 0.1935483870967742

### Agents

| agent | decisions | mean conf | low-conf ratio | handoff-layer low | ungrounded-arg ratio | tool calls | error | empty | repeat | schema | ignored |
|---|---|---|---|---|---|---|---|---|---|---|---|
| db_agent | 420 | 0.95 | 0.08 | - | 0.20 | 357 | 0.18 | 0.00 | 0.33 | 0.00 | 0.01 |
| planner | 431 | 0.90 | 0.10 | 0.10 | 0.04 | 400 | 0.09 | 0.00 | 0.03 | 0.00 | 0.08 |
| policy_checker | 55 | 0.84 | 0.27 | - | - | 19 | 0.05 | 0.58 | 0.05 | 0.00 | 0.05 |

### Handoff edges

| edge | n | mean fidelity | low(<0.8) ratio | top missing | top altered |
|---|---|---|---|---|---|
| db_agent:instruction->premise | 152 | 0.94 | 0.11 | [('2', 4), ('may 20th', 3), ('available', 3)] | [('departure_time_end', 2), ('departure_time_start', 2), ('verdict', 2)] |
| db_agent:report->planner | 152 | 0.42 | 0.82 | [('0', 17), ('jfk', 12), ('1', 9)] | [('verdict', 26), ('final_answer', 9), ('departure_date', 4)] |
| policy_checker:instruction->premise | 36 | 0.92 | 0.19 | [('eligible', 2), ('allowed under airline policy', 2), ("airline's policy", 1)] | [('verdict', 5), ('final_answer', 4), ('flight_type', 2)] |
| policy_checker:report->planner | 36 | 0.39 | 0.89 | [('need_info', 12), ('not_allowed', 9), ('2024-05-15 15:00:00 est', 7)] | [('verdict', 4), ('final_answer', 1), ('reservation_id', 1)] |

### Hotspots (top 5)

- db_agent: claim reservation_id without tool evidence — 111
- db_agent: get_reservation_details repeat — 67
- db_agent: claim money without tool evidence — 45
- planner: db_agent error — 31
- planner: db_agent ignored — 29

### Confidence by decision index

{
 "decisions 0-4": 0.9137665872617733,
 "decisions 5-9": 0.9142322903400146,
 "decisions 10-14": 0.916289027252323,
 "decisions 15-19": 0.9438376917908455,
 "decisions 20-24": 0.924665909271751,
 "decisions 25+": 0.9201804665860982
}
