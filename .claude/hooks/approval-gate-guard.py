#!/usr/bin/env python3
"""PreToolUse: block diet-guide.html writes until approval.md says status: approved."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

APPROVED = re.compile(r"(?im)^status:\s*approved\s*$")


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

    html_path = Path(path)
    approval = html_path.parent / "approval.md"
    if not approval.is_file():
        deny("diet-guide.html is blocked until runs/<id>/approval.md exists with 'status: approved'.")
        return 0

    text = approval.read_text(encoding="utf-8")
    if not APPROVED.search(text):
        deny("diet-guide.html is blocked: approval.md must contain the line 'status: approved'.")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
