---
name: artifact-validator
description: Checks diabetes-diet workflow artifacts for required headings, metadata, sources, and disclaimer before dependent agents run. Use after every artifact write in /plan-diet.
---

# Artifact validator

Apply this checklist to the artifact that was just written. Do not rewrite domain content; report structural issues so the owning agent can retry.

## Required headings (every Markdown artifact)

1. A single H1 title
2. `## Metadata` with `agent`, `run_id`, `generated_at`
3. `## Sources` (or a Sources subsection) with at least one bullet
4. `## Disclaimer` containing the phrase `not medical advice` (case-insensitive)

User-facing synthesis (`weekly-plan.md`) must also include `## Daily schedule` and `## Safety`.

## Citations

- Guideline and recipe claims need `https://` URLs.
- Food-data rows need an MCP/OFF/USDA/GI source (URL or `local GI table`).
- `User-confirmed intake` is an allowed source only on `requirements.md`.

## Predictable structure

Heading names should match the owning agent's template in `.claude/agents/`. Extra sections are allowed; missing required sections fail the check.

## Output

Return:

```
artifact: <path>
structural_pass: true|false
citation_pass: true|false
missing:
- ...
```

If either pass is false, the coordinator must not start dependent agents.
