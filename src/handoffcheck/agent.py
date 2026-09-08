"""The coding agent: writes a contract test suite for a handoff.

Workspace per boundary (in memory + mirrored to work/<id>/ for audit):
  context.txt         sender context (read-only)
  obligations.json    obligations to cover (read-only)
  fixtures/pos_<id>.txt   evidence span per obligation (read-only)
  self_tests.json     agent-written positive/negative samples (written once, then LOCKED)
  helpers.py          agent-written normalization helpers
  test_contract.py    agent-written suite: one `test_ob_<id>(message)` per obligation

Tools: read_file, grep, write_file, run_tests, submit.  One ACTION per turn:
  ACTION: {"tool": "grep", "pattern": "...", "path": "context.txt"}
  ACTION: {"tool": "write_file", "path": "test_contract.py"}   followed by a ```python fenced block
Acceptance: `submit` runs a held-out battery the agent never sees; per-test accept/reject.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from .battery import battery as battery_cases
from .llm import LLM, parse_json_lenient
from .sandbox import check_ast, check_memorization, run_suite
from .schema import Obligation, to_dict

STRATEGY_GUIDE = """Type-specific checking strategy (domain-agnostic):
- constraint (numeric/bound): parse numbers, units and the bound direction (max/min/exact) from the message and assert the CONDITION is preserved — not merely that the number appears. A cap that became "approximately" or lost its bound word is a violation. Normalize currency symbols, thousands separators, "k", number words, 12h/24h times.
- prohibition: the forbidden action must still be NEGATED near its mention ("do not cancel", "never share"). The action word appearing without negation is a violation.
- open_question: the item must still be marked as unresolved/unknown/to-confirm. If the message asserts it as settled, that is a violation.
- verified_fact / goal / ids / names: normalized presence (case, whitespace, punctuation, separators, unit spelling, ordering of clauses). A hedged fact ("probably X") counts as violated for verified_fact.
Write small, readable helpers in helpers.py (e.g. numbers(text), has_negation_near(text, term), mentions(text, *forms)) and use them from the tests. Never hardcode whole sentences; match the obligation's essential tokens/values with normalization.
"""

TOOL_GUIDE = """Tools (exactly ONE action per reply, as the LAST line `ACTION: {...}` plus an optional fenced block right after it):
- {"tool":"read_file","path":"context.txt","start_line":1,"end_line":80}
- {"tool":"grep","pattern":"<python regex>","path":"context.txt","max_hits":20}   (case-insensitive)
- {"tool":"write_file","path":"self_tests.json"}   + ```json block   (allowed ONCE; locked afterwards)
- {"tool":"write_file","path":"helpers.py"}        + ```python block
- {"tool":"write_file","path":"test_contract.py"}  + ```python block
- {"tool":"run_tests","target":"fixtures"}   runs each test_ob_<id> on its own fixture (must pass)
- {"tool":"run_tests","target":"self_tests"} runs your self_tests (positives must pass, negatives must fail)
- {"tool":"run_tests","target":"text"} + ```text block   runs all tests on that text
- {"tool":"submit"}   grades the suite on a held-out battery you cannot see; you get per-test pass/fail counts only
Rules: Python 3.11, imports limited to re, json, math, string, unicodedata, difflib, typing, collections, itertools, functools, helpers. No eval/exec/open/getattr/dunder access. Each test: `def test_ob_<id>(message: str):` and must `assert <cond>, "<diagnosis: what is missing or changed>"`.
self_tests.json format: {"positives":[{"ob":"<id>","text":"<a paraphrase of the evidence that PRESERVES the obligation>"}],
                         "negatives":[{"ob":"<id>","text":"<a version that VIOLATES it>","kind":"deleted|altered|weakened|negation_flipped|asserted"}]}
Provide >= 2 positives (real paraphrases: different units/wording/order) and >= 2 negatives per obligation. Write self_tests.json BEFORE helpers.py / test_contract.py.
Workflow: (1) grep the context for each key value to see its surface forms; (2) write self_tests.json; (3) write helpers.py and test_contract.py; (4) run_tests fixtures and self_tests until green; (5) submit. If submit rejects some tests, fix and submit again (max 3 submits).
"""

SYSTEM_PROMPT = """You are a coding agent. Your job: write a CONTRACT TEST SUITE for a handoff message.
An upstream agent is about to hand its work to another agent. The sender's context (everything it knows) is in context.txt.
A list of OBLIGATIONS extracted from that context is given: facts, constraints, open questions, prohibitions and goals that MUST survive in the outgoing handoff message. The message will be checked by running your suite on it: a failing test means the message dropped or corrupted that obligation; the assertion message is the diagnosis shown to the sender.
Your tests must be robust to paraphrase (the message is written in prose, with different wording/units/order than the context) and strict about meaning (a weakened constraint, a dropped negation, an unresolved item asserted as resolved are violations).
""" + STRATEGY_GUIDE + "\n" + TOOL_GUIDE

ACTION_RE = re.compile(r"^ACTION:\s*(\{.*\})\s*$", re.M)
FENCE_RE = re.compile(r"```(?:python|json|text|py)?\s*\n(.*?)```", re.S)


@dataclass
class AgentResult:
    boundary_id: str
    suite: str = ""
    helpers: str = ""
    self_tests: dict | None = None
    accepted: dict = field(default_factory=dict)      # ob_id -> bool
    battery_report: dict = field(default_factory=dict)  # ob_id -> {"pass": n, "fail": n, "detail": [...]} (last submit)
    steps: int = 0
    submits: int = 0
    first_submit_accept_rate: float | None = None
    uncheckable_reason: dict = field(default_factory=dict)
    memorization_rejections: int = 0
    transcript: list = field(default_factory=list)
    elapsed: float = 0.0
    error: str | None = None


class ContractAgent:
    def __init__(self, llm: LLM, *, max_steps: int = 12, extra_after_submit: int = 4, max_submits: int = 3,
                 work_dir: str | Path = "work", python: str | None = None, thinking: bool = False,
                 target_name: str = "message"):
        self.llm = llm
        self.max_steps = max_steps
        self.extra_after_submit = extra_after_submit
        self.max_submits = max_submits
        self.work_dir = Path(work_dir)
        self.python = python
        self.thinking = thinking
        self.target_name = target_name  # "message" for contract suites, "context" for grounding suites

    # ---------- public ----------
    def run(self, boundary_id: str, context_text: str, obligations: list[Obligation], *,
            item_label: str = "obligation") -> AgentResult:
        t0 = time.time()
        res = AgentResult(boundary_id=boundary_id)
        ws = {"context.txt": context_text,
              "obligations.json": json.dumps([_ob_public(o) for o in obligations], ensure_ascii=False, indent=1)}
        fixtures = {o.id: o.evidence for o in obligations}
        locked_self_tests: dict | None = None
        helpers = ""
        suite = ""
        submits = 0
        budget = self.max_steps
        ctx_lines = context_text.count("\n") + 1
        intro = (f"Workspace files: context.txt ({ctx_lines} lines), obligations.json, fixtures/pos_<id>.txt for each {item_label}.\n"
                 f"Test functions must be named test_ob_<id>(message) where message is the text under test "
                 f"(here: the {'outgoing handoff message' if self.target_name == 'message' else 'sender context'}).\n\n"
                 f"obligations.json:\n{ws['obligations.json']}\n\nStart with step (1).")
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": intro}]
        step = 0
        sample = 0
        while step < budget:
            step += 1
            out = self.llm.chat(messages, temperature=0.0 if sample == 0 else 0.3, max_tokens=3000,
                                sample_idx=sample, thinking=self.thinking, tag="agent_turn")
            text = out["text"]
            messages.append({"role": "assistant", "content": text})
            action, block = parse_action(text)
            if action is None:
                sample += 1
                messages.append({"role": "user", "content": "No valid ACTION line found. Reply with exactly one `ACTION: {...}` line (plus a fenced block if needed)."})
                if sample > 3:
                    res.error = "no valid action after retries"
                    break
                continue
            sample = 0
            tool = action.get("tool")
            reply = ""
            if tool == "read_file":
                reply = tool_read(ws, action)
            elif tool == "grep":
                reply = tool_grep(ws, action)
            elif tool == "write_file":
                path = action.get("path", "")
                if block is None:
                    reply = "write_file needs a fenced block with the file content."
                elif path == "self_tests.json":
                    if locked_self_tests is not None:
                        reply = "self_tests.json is LOCKED (already written). Continue with helpers.py / test_contract.py."
                    else:
                        obj = parse_json_lenient(block)
                        ok, msg = validate_self_tests(obj, [o.id for o in obligations])
                        if ok:
                            locked_self_tests = obj
                            res.self_tests = obj
                            reply = f"self_tests.json written and locked ({len(obj['positives'])} positives, {len(obj['negatives'])} negatives)."
                        else:
                            reply = f"self_tests.json rejected: {msg}"
                elif path == "helpers.py":
                    bad = check_ast(block)
                    reply = f"helpers.py rejected by static check: {bad}" if bad else "helpers.py written."
                    if not bad:
                        helpers = block
                elif path == "test_contract.py":
                    if locked_self_tests is None:
                        reply = "Write self_tests.json first (it is locked once written), then test_contract.py."
                    else:
                        bad = check_ast(block)
                        if bad:
                            reply = f"test_contract.py rejected by static check: {bad}"
                        else:
                            mem = check_memorization(block + "\n" + helpers, _protected_texts(locked_self_tests),
                                                     _mem_threshold(obligations))
                            if mem:
                                res.memorization_rejections += 1
                                reply = ("test_contract.py rejected: string constants copy long spans of your own test texts. "
                                         "Match essential tokens/values with normalization instead. " + "; ".join(mem[:3]))
                            else:
                                suite = block
                                missing = [o.id for o in obligations if f"def test_ob_{o.id}(" not in suite]
                                reply = "test_contract.py written." + (f" Missing tests for: {missing}" if missing else "")
                else:
                    reply = f"write_file: path {path!r} not allowed (self_tests.json, helpers.py, test_contract.py only)."
            elif tool == "run_tests":
                if not suite:
                    reply = "No test_contract.py yet."
                else:
                    reply = self._run_tests(suite, helpers, action.get("target"), block, fixtures, locked_self_tests, obligations)
            elif tool == "submit":
                if not suite:
                    reply = "Nothing to submit: write test_contract.py first."
                elif submits >= self.max_submits:
                    reply = "Submit limit reached."
                    break
                else:
                    submits += 1
                    report, accepted = self._grade(suite, helpers, obligations)
                    res.battery_report = report
                    res.accepted = accepted
                    rate = sum(accepted.values()) / max(1, len(accepted))
                    if submits == 1:
                        res.first_submit_accept_rate = rate
                        budget = step + self.extra_after_submit
                    if all(accepted.values()):
                        reply = "Submit accepted: all tests passed the held-out battery."
                        messages.append({"role": "user", "content": reply})
                        break
                    rejected = {k: v for k, v in report.items() if not accepted.get(k)}
                    summ = ", ".join(f"test_ob_{k}: {v['fail']} of {v['pass'] + v['fail']} hidden cases failed" for k, v in rejected.items())
                    reply = (f"Submit {submits}/{self.max_submits}: {sum(accepted.values())}/{len(accepted)} tests accepted. Rejected -> {summ}. "
                             "Hidden cases include paraphrases with different units/wording (must still pass) and versions with the value deleted, "
                             "a digit changed, a bound word or negation removed (must fail). Fix and submit again."
                             if submits < self.max_submits else f"Final submit: {sum(accepted.values())}/{len(accepted)} accepted.")
                    if submits >= self.max_submits:
                        messages.append({"role": "user", "content": reply})
                        break
            else:
                reply = f"Unknown tool {tool!r}."
            messages.append({"role": "user", "content": reply})
        res.steps = step
        res.submits = submits
        res.suite = suite
        res.helpers = helpers
        if not res.accepted and suite:
            # never submitted: grade once anyway so we have a verdict, counted as a submit
            report, accepted = self._grade(suite, helpers, obligations)
            res.battery_report, res.accepted = report, accepted
            res.submits += 1
            if res.first_submit_accept_rate is None:
                res.first_submit_accept_rate = sum(accepted.values()) / max(1, len(accepted))
        for o in obligations:
            if not res.accepted.get(o.id):
                res.accepted[o.id] = False
                rep = res.battery_report.get(o.id)
                res.uncheckable_reason[o.id] = ("no suite" if not suite else
                                                 ("missing test" if rep is None else f"battery: {rep.get('first_fail', '')}"))
        res.transcript = messages
        res.elapsed = time.time() - t0
        self._mirror(boundary_id, ws, locked_self_tests, helpers, suite, res)
        return res

    # ---------- tools ----------
    def _run_tests(self, suite, helpers, target, block, fixtures, self_tests, obligations) -> str:
        if target == "fixtures":
            targets = {f"pos_{k}": v for k, v in fixtures.items()}
            r = run_suite(suite, helpers, targets, python=self.python)
            if r.get("load_error") or r.get("static_errors") or r.get("process_timeout"):
                return _load_problem(r)
            lines = []
            for k in fixtures:
                st = r["targets"].get(f"pos_{k}", {}).get(f"test_ob_{k}")
                if st is None:
                    lines.append(f"test_ob_{k}: MISSING")
                else:
                    lines.append(f"test_ob_{k} on pos_{k}: {st['status']}" + (f" ({st['message']})" if st['status'] != 'pass' else ""))
            return "fixtures:\n" + "\n".join(lines)
        if target == "self_tests":
            if not self_tests:
                return "No self_tests.json."
            targets = {}
            expect = []
            for i, p in enumerate(self_tests.get("positives", [])):
                targets[f"p{i}"] = p["text"]; expect.append((f"p{i}", p["ob"], True))
            for i, n in enumerate(self_tests.get("negatives", [])):
                targets[f"n{i}"] = n["text"]; expect.append((f"n{i}", n["ob"], False))
            r = run_suite(suite, helpers, targets, python=self.python)
            if r.get("load_error") or r.get("static_errors") or r.get("process_timeout"):
                return _load_problem(r)
            ok = 0; bad = []
            for name, ob, want_pass in expect:
                st = r["targets"].get(name, {}).get(f"test_ob_{ob}")
                if st is None:
                    bad.append(f"{name}: test_ob_{ob} MISSING"); continue
                passed = st["status"] == "pass"
                if passed == want_pass:
                    ok += 1
                else:
                    bad.append(f"{name} (ob {ob}, expected {'pass' if want_pass else 'fail'}): got {st['status']} {st['message'][:80]} | text: {targets[name][:120]!r}")
            return f"self_tests: {ok}/{len(expect)} as expected." + ("\n" + "\n".join(bad[:12]) if bad else "")
        if target == "text":
            if block is None:
                return "run_tests text needs a fenced block."
            r = run_suite(suite, helpers, {"text": block}, python=self.python)
            if r.get("load_error") or r.get("static_errors") or r.get("process_timeout"):
                return _load_problem(r)
            return "\n".join(f"{k}: {v['status']} {v['message']}" for k, v in r["targets"]["text"].items())
        return "run_tests target must be fixtures | self_tests | text."

    def _grade(self, suite: str, helpers: str, obligations: list[Obligation]) -> tuple[dict, dict]:
        """Held-out battery per obligation. Returns (report, accepted)."""
        targets = {}
        cases = []
        for o in obligations:
            for c in battery_cases(o):
                name = f"{o.id}::{c['name']}"
                targets[name] = c["text"]
                cases.append((o.id, name, c["expected"]))
        r = run_suite(suite, helpers, targets, python=self.python, timeout_s=60)
        report = {o.id: {"pass": 0, "fail": 0, "first_fail": ""} for o in obligations}
        accepted = {}
        if r.get("load_error") or r.get("static_errors") or r.get("process_timeout"):
            for o in obligations:
                report[o.id]["first_fail"] = _load_problem(r)[:120]
                accepted[o.id] = False
            return report, accepted
        for ob_id, name, want_pass in cases:
            st = r["targets"].get(name, {}).get(f"test_ob_{ob_id}")
            if st is None:
                report[ob_id]["fail"] += 1
                report[ob_id]["first_fail"] = report[ob_id]["first_fail"] or "missing test"
                continue
            passed = st["status"] == "pass"
            if passed == want_pass:
                report[ob_id]["pass"] += 1
            else:
                report[ob_id]["fail"] += 1
                if not report[ob_id]["first_fail"]:
                    report[ob_id]["first_fail"] = f"{name.split('::')[1]} expected {'pass' if want_pass else 'fail'} got {st['status']}"
        for o in obligations:
            accepted[o.id] = report[o.id]["fail"] == 0 and report[o.id]["pass"] > 0
        return report, accepted

    def _mirror(self, boundary_id, ws, self_tests, helpers, suite, res: AgentResult) -> None:
        d = self.work_dir / boundary_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "context.txt").write_text(ws["context.txt"])
        (d / "obligations.json").write_text(ws["obligations.json"])
        if self_tests is not None:
            (d / "self_tests.json").write_text(json.dumps(self_tests, ensure_ascii=False, indent=1))
        (d / "helpers.py").write_text(helpers)
        (d / "test_contract.py").write_text(suite)
        (d / "transcript.json").write_text(json.dumps(res.transcript, ensure_ascii=False, indent=1))
        (d / "result.json").write_text(json.dumps({k: v for k, v in to_dict(res).items() if k != "transcript"}, ensure_ascii=False, indent=1))


# ---------- helpers ----------

def parse_action(text: str) -> tuple[dict | None, str | None]:
    m = None
    for m in ACTION_RE.finditer(text):
        pass
    if m is None:
        return None, None
    action = parse_json_lenient(m.group(1))
    if not isinstance(action, dict):
        return None, None
    block = None
    after = text[m.end():]
    fm = FENCE_RE.search(after)
    if fm:
        block = fm.group(1)
    else:
        # allow the fenced block BEFORE the action line (models often do that)
        before = text[:m.start()]
        fms = list(FENCE_RE.finditer(before))
        if fms:
            block = fms[-1].group(1)
    return action, block


def tool_read(ws: dict, a: dict) -> str:
    path = a.get("path", "context.txt")
    if path not in ws:
        return f"read_file: no such file {path!r}. Files: {sorted(ws)}"
    lines = ws[path].splitlines()
    s = max(1, int(a.get("start_line", 1) or 1)); e = min(len(lines), int(a.get("end_line", s + 79) or (s + 79)))
    e = min(e, s + 199)
    body = "\n".join(f"{i:4d}| {lines[i-1]}" for i in range(s, e + 1))
    return f"{path} lines {s}-{e} of {len(lines)}:\n{body}"


def tool_grep(ws: dict, a: dict) -> str:
    path = a.get("path", "context.txt")
    if path not in ws:
        return f"grep: no such file {path!r}."
    pat = a.get("pattern", "")
    try:
        rx = re.compile(pat, re.I)
    except re.error as e:
        return f"grep: bad regex: {e}"
    hits = []
    mx = int(a.get("max_hits", 20) or 20)
    for i, line in enumerate(ws[path].splitlines(), 1):
        if rx.search(line):
            hits.append(f"{i:4d}| {line[:240]}")
            if len(hits) >= mx:
                break
    return f"grep {pat!r}: {len(hits)} hit(s)" + (":\n" + "\n".join(hits) if hits else "")


def validate_self_tests(obj, ob_ids: list[str]) -> tuple[bool, str]:
    if not isinstance(obj, dict) or "positives" not in obj or "negatives" not in obj:
        return False, "must be an object with 'positives' and 'negatives' arrays"
    ids = set(ob_ids)
    for key in ("positives", "negatives"):
        if not isinstance(obj[key], list):
            return False, f"{key} must be a list"
        for it in obj[key]:
            if not isinstance(it, dict) or str(it.get("ob")) not in ids or not isinstance(it.get("text"), str) or not it["text"].strip():
                return False, f"each {key[:-1]} needs 'ob' (one of {sorted(ids)}) and non-empty 'text'"
            it["ob"] = str(it["ob"])
    for oid in ob_ids:
        np_ = sum(1 for p in obj["positives"] if p["ob"] == oid)
        nn_ = sum(1 for n in obj["negatives"] if n["ob"] == oid)
        if np_ < 2 or nn_ < 2:
            return False, f"obligation {oid} needs >= 2 positives and >= 2 negatives (has {np_}/{nn_})"
    return True, ""


def _protected_texts(self_tests: dict | None) -> list[str]:
    if not self_tests:
        return []
    return [x["text"] for x in self_tests.get("positives", []) + self_tests.get("negatives", [])]


def _mem_threshold(obligations: list[Obligation]) -> int:
    longest_kv = max((len(kv) for o in obligations for kv in o.key_values), default=0)
    return max(30, longest_kv + 10)


def _ob_public(o: Obligation) -> dict:
    d = {"id": o.id, "type": o.type, "statement": o.statement, "key_values": o.key_values, "evidence": o.evidence}
    if o.numeric:
        d["numeric"] = o.numeric
    if o.negated:
        d["negated"] = True
    return d


def _load_problem(r: dict) -> str:
    if r.get("static_errors"):
        return "static check failed: " + "; ".join(r["static_errors"][:5])
    if r.get("process_timeout"):
        return "the whole test process timed out (runaway regex or loop)."
    return f"suite failed to load: {r.get('load_error')}"


# ---------- runtime: apply an accepted suite to a message ----------

def run_contract(suite: str, helpers: str, text: str, accepted: dict[str, bool], obligation_ids: list[str],
                 python: str | None = None) -> dict[str, dict]:
    """Returns {ob_id: {"status": preserved|violated|uncheckable, "diagnosis": str}}."""
    out = {}
    if not suite:
        return {oid: {"status": "uncheckable", "diagnosis": "no suite"} for oid in obligation_ids}
    r = run_suite(suite, helpers, {"t": text}, python=python)
    res = r.get("targets", {}).get("t", {})
    for oid in obligation_ids:
        if not accepted.get(oid):
            out[oid] = {"status": "uncheckable", "diagnosis": "test not accepted by battery"}
            continue
        st = res.get(f"test_ob_{oid}")
        if st is None:
            out[oid] = {"status": "uncheckable", "diagnosis": _load_problem(r) if not res else "missing test"}
        elif st["status"] == "pass":
            out[oid] = {"status": "preserved", "diagnosis": ""}
        elif st["status"] == "fail":
            out[oid] = {"status": "violated", "diagnosis": st["message"]}
        else:
            out[oid] = {"status": "uncheckable", "diagnosis": f"{st['status']}: {st['message']}"}
    return out


# ---------- ablation: one-shot, no tools, no self-validation ----------

ONESHOT_PROMPT = """You are a coding agent. Write a contract test suite for a handoff message. """ + STRATEGY_GUIDE + """
Output exactly two fenced python blocks: first `helpers.py`, then `test_contract.py` with one `def test_ob_<id>(message: str)` per obligation, each ending in `assert <cond>, "<diagnosis>"`. Imports limited to re, json, math, string, unicodedata, difflib, typing, collections, itertools, functools, helpers. No other text."""


def synthesize_oneshot(llm: LLM, boundary_id: str, context_text: str, obligations: list[Obligation], *,
                       python: str | None = None, thinking: bool = False) -> AgentResult:
    t0 = time.time()
    res = AgentResult(boundary_id=boundary_id)
    obl = json.dumps([_ob_public(o) for o in obligations], ensure_ascii=False, indent=1)
    ctx = context_text if len(context_text) < 12000 else context_text[:6000] + "\n...\n" + context_text[-6000:]
    msgs = [{"role": "system", "content": ONESHOT_PROMPT},
            {"role": "user", "content": f"Sender context (excerpt):\n{ctx}\n\nObligations:\n{obl}\n\nWrite helpers.py then test_contract.py."}]
    out = llm.chat(msgs, temperature=0.0, max_tokens=3000, thinking=thinking, tag="oneshot")
    blocks = FENCE_RE.findall(out["text"])
    helpers, suite = ("", "") if not blocks else ((blocks[0], blocks[1]) if len(blocks) >= 2 else ("", blocks[0]))
    if "def test_ob_" in helpers and "def test_ob_" not in suite:
        helpers, suite = suite, helpers
    res.helpers, res.suite, res.steps, res.submits = helpers, suite, 1, 0
    bad = check_ast(suite) + (check_ast(helpers) if helpers else [])
    r = run_suite(suite, helpers, {"probe": "x"}, python=python) if not bad else {"load_error": "static"}
    loaded = not bad and not r.get("load_error") and not r.get("process_timeout")
    for o in obligations:
        has = loaded and f"test_ob_{o.id}" in r.get("tests", [])
        res.accepted[o.id] = bool(has)
        if not has:
            res.uncheckable_reason[o.id] = "static/load failure" if not loaded else "missing test"
    res.elapsed = time.time() - t0
    res.transcript = msgs + [{"role": "assistant", "content": out["text"]}]
    return res
