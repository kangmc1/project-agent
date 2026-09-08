"""Document checklist gates (P12, P12b, P13, P16).  Usage: python scripts/check_docs.py --skeleton|--proposal|--slides|--adr"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def has(text: str, *needles: str) -> list[str]:
    return [n for n in needles if n not in text]


def check_skeleton() -> list[str]:
    t = Path("docs/proposal.md").read_text(encoding="utf-8")
    missing = has(t, "## 1. 배경", "## 2. 기존 연구", "## 3. 제안", "## 4. 결과 및 평가", "<!-- TABLE: metrics", "<!-- FIGURE: recovery.png")
    return [f"proposal skeleton missing: {m}" for m in missing]


def check_proposal() -> list[str]:
    t = Path("docs/proposal.md").read_text(encoding="utf-8")
    problems = []
    problems += [f"section missing: {m}" for m in has(t, "## 1. 배경", "## 2. 기존 연구", "## 3. 제안", "## 4. 결과 및 평가", "기대 효과", "한계")]
    problems += [f"4-type table missing: {m}" for m in has(t, "| handoff 문제", "| 도구 사용 실패", "| 환각", "| 추론 오류")]
    problems += [f"module design missing: {m}" for m in has(t, "**D1", "**D2", "**D3", "**D4", "D8", "D10", "D6")]
    problems += [f"AC-15 item missing: {m}" for m in has(t, "환각/추론 개별 판정", "subtag")]
    lim = ["60회", "단일 실행 모델", "시뮬레이터", "라벨러", "순차", "완전 관측", "일반화", "미구현", "커버리지", "주입 프롬프트", "삭제", "bf16"]
    problems += [f"limitation missing: {m}" for m in has(t, *lim)]
    problems += [f"spec deviation footnote missing: {m}" for m in has(t, "이탈")]
    if "SKELETON" in t:
        problems.append("still marked SKELETON")
    if "(M6 이후 채움)" in t or "(M8에 작성" in t:
        problems.append("placeholders remain")
    if not re.search(r"\| .*AUROC", t):
        problems.append("no results table with AUROC")
    problems += [f"framing missing: {m}" for m in has(t, "Align")]
    return problems


def check_slides() -> list[str]:
    # slides dropped by user decision (2026-09-09 07:40): written submission only
    return []


def _check_slides_legacy() -> list[str]:
    p = Path("docs/slides.html")
    if not p.exists():
        return ["docs/slides.html missing"]
    t = p.read_text(encoding="utf-8")
    problems = [f"slides missing: {m}" for m in has(t, "planner", "auditor", "AUROC", "한계")]
    readme = Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else ""
    if "claude.ai/code/artifact" not in readme and "slides.html" not in readme:
        problems.append("README lacks slides link")
    return problems


def check_adr() -> list[str]:
    t = Path(".omc/plans/agent-failure-detection-plan.md").read_text(encoding="utf-8")
    problems = [f"ADR missing: {m}" for m in has(t, "## 7. ADR", "**Decision**", "**Drivers**", "**Alternatives", "**Why", "**Consequences**", "**Follow-ups**")]
    if not Path("docs/notes/timeline.md").exists():
        problems.append("timeline.md missing")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    for f in ("skeleton", "proposal", "slides", "adr"):
        ap.add_argument(f"--{f}", action="store_true")
    a = ap.parse_args()
    problems = []
    if a.skeleton:
        problems += check_skeleton()
    if a.proposal:
        problems += check_proposal()
    if a.slides:
        problems += check_slides()
    if a.adr:
        problems += check_adr()
    for p in problems:
        print("[FAIL]", p)
    print("OK" if not problems else f"{len(problems)} problems")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
