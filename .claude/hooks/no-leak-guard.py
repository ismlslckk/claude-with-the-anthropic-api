#!/usr/bin/env python3
"""PreToolUse: keep internal artifact filenames out of user-facing HTML."""

from __future__ import annotations

import json
import sys

LEAKS = (
    "artifacts/",
    "workflow-state.json",
    "requirements.md",
    "guidelines.md",
    "food-data.md",
    "meal-plan.md",
    "recipes.md",
    "grocery-list.md",
    "timing.md",
    "budget.md",
    "validation.md",
    "weekly-plan.md",
    "approval.md",
    "CLAUDE.md",
    ".claude/",
    "coordinator.md",
)


def deny(reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input") or {}
    path = str(tool_input.get("file_path") or tool_input.get("path") or "")
    if not path.endswith("diet-guide.html"):
        return 0

    content = str(tool_input.get("content") or tool_input.get("new_string") or "")
    found = [token for token in LEAKS if token in content]
    if found:
        deny(
            "diet-guide.html must not mention internal files: "
            + ", ".join(found)
            + ". Rewrite using human-facing section titles only."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
