# Diabetes diet agentic workflow

A Claude Code hub-and-spoke workflow that turns a confirmed diabetes meal-planning request into a weekly HTML guide. It uses specialized subagents, reusable skills, PreToolUse/PostToolUse hooks, web search, and a custom nutrition MCP server.

**This is an educational project. It is not medical advice, diagnosis, or a substitute for a clinician or registered dietitian.**

Course notebooks and earlier API exercises live in [`anthropic-api-course/`](anthropic-api-course/).

## Prerequisites

- [Claude Code](https://code.claude.com/docs/en/quickstart) CLI (`claude` or `npx @anthropic-ai/claude-code`)
- Python 3.10+ (a project venv at `mcp/.venv` is enough to launch the nutrition MCP)
- Network access for WebSearch and Open Food Facts

Optional:

- `USDA_API_KEY` for USDA FoodData Central (Open Food Facts and the local GI table work without it)

## Setup from a clean checkout

```bash
git clone <this-repo>
cd claude-with-the-anthropic-api
cp .env.example .env
# optionally edit .env and add USDA_API_KEY
python3.12 -m venv mcp/.venv
mcp/.venv/bin/pip install -e mcp
```

Confirm Claude Code sees the project MCP server:

```bash
claude mcp list
```

You should see `nutrition`. If the project MCP is not picked up, add it once:

```bash
claude mcp add nutrition -- "$PWD/mcp/.venv/bin/python" "$PWD/mcp/nutrition_server.py"
```

Do not commit `.env`, API keys, or `.claude/settings.local.json`.

## Run

From the repository root:

```bash
npx @anthropic-ai/claude-code
```

If the `claude` CLI is already installed, this is equivalent:

```bash
claude
```

Then invoke the slash command with the request, for example:

```text
/plan-diet Plan a 7-day vegetarian diet for newly diagnosed type 2 diabetes. Metformin 500 mg twice daily. Budget $80/week.
```

The command instantiates the **coordinator**. It will ask for any missing requirements, confirm them, then run subagents (parallel where independent). It stops for **human approval** before writing `diet-guide.html`.

To approve, ensure `runs/<run-id>/approval.md` contains:

```text
status: approved
```

A PreToolUse hook blocks the HTML write until that line is present. Rejected plans are revised and submitted for approval again.

## Resume

Workflow state is `runs/<run-id>/workflow-state.json`. Completed agents are skipped.

Resume by pointing at the same run:

```text
/plan-diet Resume run 01-type2-vegetarian and continue remaining work.
```

Interrupted or retried work continues from persisted artifacts. Downstream files are regenerated only when a quality gate or rejection requires it.

## Sample runs

Three captured runs are committed under `runs/`:

| Run | Scenario | Extra agents |
|-----|----------|----------------|
| [`01-type2-vegetarian`](runs/01-type2-vegetarian/) | Type 2, metformin, lacto-ovo vegetarian, $80 budget | budget-aggregator |
| [`02-type1-athlete`](runs/02-type1-athlete/) | Type 1, insulin pump, endurance training | glucose-timing-advisor |
| [`03-type2-limited-cooking`](runs/03-type2-limited-cooking/) | Older adult, one-pot/microwave, sodium cap, $50 budget | budget-aggregator |

Each folder includes `input.md`, `artifacts/`, `workflow-state.json`, `approval.md`, and `diet-guide.html`.

## Layout

```text
.claude/commands/plan-diet.md   # /plan-diet
.claude/agents/                 # coordinator + domain subagents
.claude/skills/                 # artifact-validator, diet-html-theme-builder
.claude/hooks/                  # approval, no-leak, post-write state
.claude/settings.json           # PreToolUse + PostToolUse
.mcp.json                       # nutrition MCP
mcp/nutrition_server.py         # FastMCP server
CLAUDE.md                       # execution rules
runs/                           # sample + live runs
```

## Secrets

| Variable | Required | Purpose |
|----------|----------|---------|
| Claude Code login | yes | Model access (not stored in this repo) |
| `USDA_API_KEY` | no | USDA lookups in the nutrition MCP |

`.gitignore` excludes `.env` and `.claude/settings.local.json`.
