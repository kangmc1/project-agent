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
| solver:instruction->premise | 43 | 0.84 | 0.26 | [('final integer answer', 5), ('key equations used', 2), ('Provide a complete solution with the final integer answer and the key equations used.', 2)] | [] |
| solver:report->planner | 43 | 0.16 | 0.95 | [('n = 1', 2), ('distance from the school to the park is 252/25 miles', 1), ('m = 252', 1)] | [] |
| verifier:instruction->premise | 29 | 0.80 | 0.43 | [('final integer answer', 1), ('key equations used', 1), ('Problem is AIME problem', 1)] | [('The operation is not associative; must evaluate step by step.', 1)] |
| verifier:report->planner | 29 | 0.23 | 0.93 | [('distance from the school to the park is 252/25 miles', 2), ('m + n = 277', 2), ('even-length palindrome construction formula', 1)] | [('279 positive integers n less than 1000 such that f(n) = n', 1)] |

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
| db_agent:instruction->premise | 152 | 0.90 | 0.16 | [('Date: May 24', 3), ('Option: second cheapest economy class option', 2), ('Passenger 1: Sophia Silva', 2)] | [('retrieve current business class price', 1), ('retrieve current economy class price', 1), ('Retrieve exact economy class prices for each reservation', 1)] |
| db_agent:report->planner | 152 | 0.44 | 0.83 | [('Flight Type: one_way', 7), ('Cabin: basic_economy', 5), ('booking failed', 4)] | [('error type', 1), ('The available one-stop flights depart much earlier or later than the requested time window.', 1), ('HAT218 connecting flight arrival time 03:00+1 (3:00 AM next day)', 1)] |
| policy_checker:instruction->premise | 36 | 0.97 | 0.06 | [('The check is under the current airline policy.', 1), ('policy check', 1)] | [('User is checking eligibility to pay a fee to change flight', 1)] |
| policy_checker:report->planner | 36 | 0.49 | 0.86 | [('User ID: amelia_rossi_1247', 2), ('Requested action: Cancel flights due to a change in travel plans', 2), ('The current date is 2024-05-15 15:00:00 EST.', 2)] | [('The user is asking about the typical price difference between business and economy class for five reservations: JG7FMM, 2FBBAH, X7BYG1, EQ1G6C, BOH180.', 1), ('reservation ID unknown', 1), ("The number of free checked bags depends on the customer's membership tier and cabin class.", 1)] |

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
