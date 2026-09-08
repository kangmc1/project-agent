"""Sandboxed execution of agent-written test suites.

- Static gate: AST import whitelist + banned names + no dunder attribute access.
- Dynamic: separate `python -I -S` process, RLIMITs, per-case timer, whole-process timeout with parent kill.
- Memorization check: string/regex constants that copy long spans of the agent's own test texts are rejected.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ALLOWED_MODULES = {"re", "json", "math", "string", "unicodedata", "difflib", "typing", "collections",
                   "itertools", "functools", "helpers"}
BANNED_NAMES = {"eval", "exec", "__import__", "getattr", "setattr", "delattr", "compile", "open", "input",
                "globals", "locals", "vars", "breakpoint", "exit", "quit", "memoryview", "help", "dir"}


def check_ast(code: str) -> list[str]:
    """Return a list of violations (empty = ok)."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"syntax error: {e}"]
    bad: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in ALLOWED_MODULES:
                    bad.append(f"import not allowed: {a.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED_MODULES:
                bad.append(f"import not allowed: from {node.module}")
        elif isinstance(node, ast.Name) and node.id in BANNED_NAMES:
            bad.append(f"banned name: {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            bad.append(f"dunder attribute access: {node.attr}")
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            bad.append("global/nonlocal not allowed")
    return bad


def string_constants(code: str) -> list[str]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


_ws = re.compile(r"\s+")


def _n(s: str) -> str:
    return _ws.sub(" ", s).strip().casefold()


def check_memorization(code: str, protected_texts: list[str], max_span: int) -> list[str]:
    """Reject constants that reproduce a span of any protected text longer than max_span characters."""
    bad = []
    prot = [_n(t) for t in protected_texts if t]
    for c in string_constants(code):
        cn = _n(c)
        if len(cn) <= max_span:
            continue
        # a regex pattern: strip common metachars for the comparison
        cn2 = re.sub(r"[\\^$.*+?()\[\]{}|]", "", cn)
        for t in prot:
            if cn in t or (len(cn2) > max_span and cn2 in t):
                bad.append(f"constant copies protected text: {c[:60]!r}")
                break
    return bad


_DRIVER = r'''
import sys, json, resource, signal, types, traceback
resource.setrlimit(resource.RLIMIT_AS, (768*1024*1024, 768*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
try:
    resource.setrlimit(resource.RLIMIT_NPROC, (8, 8))
except Exception:
    pass
resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
spec = json.load(sys.stdin)
per_case = float(spec.get("per_case_s", 0.5))

class CaseTimeout(Exception):
    pass

def _alarm(signum, frame):
    raise CaseTimeout()
signal.signal(signal.SIGALRM, _alarm)

safe_builtins = {k: v for k, v in __builtins__.__dict__.items()} if hasattr(__builtins__, "__dict__") else dict(__builtins__)
for k in ["eval", "exec", "__import__", "open", "input", "compile", "globals", "locals", "vars", "breakpoint", "exit", "quit", "help"]:
    safe_builtins.pop(k, None)
real_import = __import__
ALLOWED = set(spec.get("allowed_modules", []))
def guarded_import(name, *a, **k):
    if name.split(".")[0] not in ALLOWED:
        raise ImportError("import not allowed: " + name)
    return real_import(name, *a, **k)
safe_builtins["__import__"] = guarded_import

def load_module(name, code):
    m = types.ModuleType(name)
    m.__dict__["__builtins__"] = safe_builtins
    sys.modules[name] = m
    exec(compile(code, name + ".py", "exec"), m.__dict__)
    return m

result = {"targets": {}, "load_error": None, "tests": []}
try:
    if spec.get("helpers"):
        load_module("helpers", spec["helpers"])
    suite = load_module("test_contract", spec["suite"])
    tests = [(n, f) for n, f in vars(suite).items() if n.startswith("test_") and callable(f)]
    tests.sort(key=lambda x: x[0])
    result["tests"] = [n for n, _ in tests]
except BaseException as e:
    result["load_error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    print(json.dumps(result)); sys.exit(0)

for tname, text in spec["targets"].items():
    out = {}
    for n, f in tests:
        signal.setitimer(signal.ITIMER_REAL, per_case)
        try:
            f(text)
            out[n] = {"status": "pass", "message": ""}
        except AssertionError as e:
            out[n] = {"status": "fail", "message": str(e)[:300]}
        except CaseTimeout:
            out[n] = {"status": "timeout", "message": "per-case timeout"}
        except BaseException as e:
            out[n] = {"status": "error", "message": "%s: %s" % (type(e).__name__, str(e)[:200])}
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
    result["targets"][tname] = out
print(json.dumps(result))
'''


def run_suite(suite: str, helpers: str | None, targets: dict[str, str], *, timeout_s: float = 20.0,
              per_case_s: float = 0.5, python: str | None = None) -> dict:
    """Run a test suite against several target texts.

    Returns {"targets": {target_name: {test_name: {"status", "message"}}}, "tests": [...], "load_error": str|None,
             "static_errors": [...], "process_timeout": bool}
    """
    static = check_ast(suite) + (check_ast(helpers) if helpers else [])
    if static:
        return {"targets": {}, "tests": [], "load_error": None, "static_errors": static, "process_timeout": False}
    spec = {"suite": suite, "helpers": helpers or "", "targets": targets, "per_case_s": per_case_s,
            "allowed_modules": sorted(ALLOWED_MODULES)}
    py = python or sys.executable
    with tempfile.TemporaryDirectory() as td:
        drv = Path(td) / "driver.py"
        drv.write_text(_DRIVER)
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONHASHSEED": "0"}
        try:
            p = subprocess.run([py, "-I", "-S", str(drv)], input=json.dumps(spec), capture_output=True, text=True,
                               timeout=timeout_s, cwd=td, env=env)
        except subprocess.TimeoutExpired:
            return {"targets": {}, "tests": [], "load_error": None, "static_errors": [], "process_timeout": True}
    if p.returncode != 0 and not p.stdout.strip():
        return {"targets": {}, "tests": [], "load_error": f"driver crashed: {p.stderr[-300:]}", "static_errors": [],
                "process_timeout": False}
    try:
        res = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return {"targets": {}, "tests": [], "load_error": f"unparseable driver output: {p.stdout[-200:]} {p.stderr[-200:]}",
                "static_errors": [], "process_timeout": False}
    res["static_errors"] = []
    res["process_timeout"] = False
    return res
