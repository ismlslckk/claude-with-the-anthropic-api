---
description: Plan a diabetes-friendly diet program. Instantiates the coordinator, gathers requirements, runs subagents, quality gates, human approval, and HTML output.
---

You are starting the diabetes diet agentic workflow. Instantiate the `coordinator` subagent and let it orchestrate the full hub-and-spoke run. Do not produce diet content yourself.

User request:
$ARGUMENTS

Follow [CLAUDE.md](CLAUDE.md) exactly:

1. Create or resume `runs/<run-id>/` and `workflow-state.json`.
2. Gather and confirm missing requirements before any domain work.
3. Spawn the `coordinator` and have it select, sequence, and retry subagents.
4. Independent agents in a stage run in parallel; dependent stages run sequentially.
5. Use WebSearch and the nutrition MCP. Do not rely on model memory alone.
6. Stop at human approval. Do not write `diet-guide.html` until `approval.md` contains `status: approved`.
