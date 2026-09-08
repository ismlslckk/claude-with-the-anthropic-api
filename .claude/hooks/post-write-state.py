#!/usr/bin/env python3
"""PostToolUse: update workflow-state.json when a run artifact is written."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_BY_FILE = {
    "requirements.md": "requirements-formalizer",
    "guidelines.md": "guideline-researcher",
    "food-data.md": "nutrition-lookup",
    "meal-plan.md": "meal-planner",
    "recipes.md": "recipe-nutritionist",
    "grocery-list.md": "grocery-planner",
    "timing.md": "glucose-timing-advisor",
    "budget.md": "budget-aggregator",
    "validation.md": "validator",
    "weekly-plan.md": "weekly-plan-builder",
    "diet-guide.html": "html-builder",
    "approval.md": None,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def find_run_dir(path: Path) -> Path | None:
    for parent in (path.parent, *path.parents):
        if parent.name == "runs":
            return None
        if parent.parent.name == "runs":
            return parent
    return None


def load_state(path: Path) -> dict:
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "run_id": path.parent.name,
        "status": "in_progress",
        "created_at": now(),
        "execution_plan": [],
        "skipped": [],
        "completed": [],
        "failed": [],
        "retries": {},
        "gates": {},
        "approval": {"status": "pending"},
        "artifacts": {},
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("path")
    if not raw:
        return 0

    written = Path(str(raw)).resolve()
    run_dir = find_run_dir(written)
    if run_dir is None:
        return 0

    name = written.name
    if name not in AGENT_BY_FILE:
        return 0

    state_path = run_dir / "workflow-state.json"
    state = load_state(state_path)
    rel = str(written.relative_to(run_dir)).replace("\\", "/")
    agent = AGENT_BY_FILE[name]

    if agent:
        state.setdefault("artifacts", {})[agent] = rel
        completed = state.setdefault("completed", [])
        if agent not in completed:
            completed.append(agent)
        failed = state.setdefault("failed", [])
        if agent in failed:
            failed.remove(agent)

    if name == "approval.md":
        text = written.read_text(encoding="utf-8") if written.is_file() else ""
        status = "pending"
        for line in text.splitlines():
            if line.lower().startswith("status:"):
                status = line.split(":", 1)[1].strip().lower()
                break
        state["approval"] = {"status": status, "updated_at": now()}

    if name == "diet-guide.html":
        state["status"] = "completed"
        state["final_output"] = rel

    if name == "validation.md" and written.is_file():
        text = written.read_text(encoding="utf-8")
        passed = None
        for line in text.splitlines():
            if "passed:" in line.lower():
                passed = "true" in line.lower()
                break
        if passed is not None:
            state["gates"] = {"passed": passed, "updated_at": now()}
            if passed is False:
                state["status"] = "needs_retry"
            elif state.get("status") == "needs_retry":
                state["status"] = "in_progress"

    state["updated_at"] = now()
    state["run_id"] = run_dir.name
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
