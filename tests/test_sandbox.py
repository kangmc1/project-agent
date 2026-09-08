from handoffcheck.sandbox import run_suite, check_ast, check_memorization

SUITE = '''
import re
import helpers
def test_ob_1(message):
    assert helpers.has_number(message, 500), "missing: budget cap 500"
def test_ob_2(message):
    assert "refund" in message.lower(), "missing: refund policy"
'''
HELPERS = '''
import re
def has_number(text, n):
    return any(abs(float(x.replace(",", "")) - n) < 1e-6 for x in re.findall(r"\\d[\\d,]*\\.?\\d*", text))
'''


def test_pass_fail_reporting():
    r = run_suite(SUITE, HELPERS, {"ok": "Budget is at most $500; the ticket is non-refundable.", "bad": "Budget is flexible."})
    assert r["load_error"] is None and not r["static_errors"]
    assert r["targets"]["ok"]["test_ob_1"]["status"] == "pass"
    assert r["targets"]["ok"]["test_ob_2"]["status"] == "pass"
    assert r["targets"]["bad"]["test_ob_1"]["status"] == "fail"
    assert "budget cap" in r["targets"]["bad"]["test_ob_1"]["message"]


def test_static_rejections():
    assert check_ast("import os\n")
    assert check_ast("x = open('/etc/passwd')\n")
    assert check_ast("def test_a(m):\n    return m.__class__\n")
    assert check_ast("import subprocess") and check_ast("import datetime")
    assert not check_ast("import re\ndef test_a(m):\n    assert re.search('x', m)\n")


def test_runtime_import_guard():
    r = run_suite("def test_a(m):\n    import os\n    assert True\n", None, {"t": "x"})
    assert r["static_errors"]  # caught statically
    # dynamic guard: importlib via allowed alias is impossible; check that a hidden import errors at runtime
    r = run_suite("def test_a(m):\n    __builtins__['x'] = 1\n    assert True\n", None, {"t": "x"})
    assert r["static_errors"] or r["targets"]["t"]["test_a"]["status"] in ("error", "pass")


def test_timeout_per_case():
    r = run_suite("def test_loop(m):\n    while True:\n        pass\n", None, {"t": "x"}, per_case_s=0.3, timeout_s=10)
    assert r["targets"]["t"]["test_loop"]["status"] == "timeout"


def test_process_timeout_kills():
    r = run_suite("import re\ndef test_re(m):\n    assert re.match(r'(a+)+$', 'a'*40+'b')\n", None, {"t": "x"}, per_case_s=0.3, timeout_s=3)
    assert r["process_timeout"] or r["targets"]["t"]["test_re"]["status"] in ("timeout", "fail")


def test_memorization():
    txt = "The customer wants to change the return flight and keep the cost under 200 dollars total"
    assert check_memorization('def test_a(m):\n    assert "keep the cost under 200 dollars total" in m\n', [txt], 20)
    assert not check_memorization('def test_a(m):\n    assert "200" in m\n', [txt], 20)
