"""Generic helpers: JSON-schema -> StructuredTool, python runner, submit tool."""
from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Callable

from langchain_core.tools import StructuredTool
from pydantic import Field, create_model

_JSON2PY = {"string": str, "integer": int, "number": float, "boolean": bool, "array": list, "object": dict}


def schema_to_model(name: str, schema: dict) -> type:
    props = (schema or {}).get("properties", {}) or {}
    required = set((schema or {}).get("required", []) or [])
    fields: dict[str, Any] = {}
    for k, v in props.items():
        typ = _JSON2PY.get((v or {}).get("type"), Any)
        desc = (v or {}).get("description", "")
        if k in required:
            fields[k] = (typ, Field(..., description=desc))
        else:
            fields[k] = (typ | None, Field(None, description=desc))
    return create_model(f"{name}_Args", **fields)  # type: ignore[call-overload]


def openai_tool_to_structured(tool_info: dict, fn: Callable[..., Any]) -> StructuredTool:
    f = tool_info["function"]
    model = schema_to_model(f["name"], f.get("parameters"))
    return StructuredTool.from_function(func=fn, name=f["name"], description=f.get("description", ""),
                                        args_schema=model, infer_schema=False)


def make_run_python(timeout: int = 10) -> StructuredTool:
    Args = create_model("run_python_Args", code=(str, Field(..., description="Python 3 code to execute; print results")))

    def run_python(code: str) -> str:
        try:
            p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=timeout)
            out = (p.stdout or "")[-4000:]
            err = (p.stderr or "")[-2000:]
            return json.dumps({"exit_code": p.returncode, "stdout": out, "stderr": err})
        except subprocess.TimeoutExpired:
            return json.dumps({"exit_code": -1, "stdout": "", "stderr": f"timeout after {timeout}s"})

    return StructuredTool.from_function(func=run_python, name="run_python",
                                        description="Execute Python code in a sandboxed subprocess (10s limit) and return stdout/stderr.",
                                        args_schema=Args, infer_schema=False)


def make_submit_answer(store: dict) -> StructuredTool:
    Args = create_model("submit_answer_Args", answer=(int, Field(..., description="Final integer answer (0-999)")))

    def submit_answer(answer: int) -> str:
        store["submitted"] = int(answer)
        return f"Answer {answer} submitted. The task is complete; reply with a one-line final statement."

    return StructuredTool.from_function(func=submit_answer, name="submit_answer",
                                        description="Submit the final integer answer. Call exactly once when confident.",
                                        args_schema=Args, infer_schema=False)


def make_think() -> StructuredTool:
    Args = create_model("think_Args", thought=(str, Field(..., description="A thought to think about.")))

    def think(thought: str) -> str:
        return ""

    return StructuredTool.from_function(func=think, name="think",
                                        description="Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log.",
                                        args_schema=Args, infer_schema=False)
