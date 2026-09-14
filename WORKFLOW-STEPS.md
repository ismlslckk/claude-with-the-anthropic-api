# How the diabetes diet workflow works (step by step)

Educational meal-planning workflow. **Not medical advice.**

This file lists every step in order and **which files are called or written**. `<run-id>` is the folder name under `runs/`, for example `20260819-type2-veg-med` or `01-type2-vegetarian`.

Start the app from the repo root:

```bash
npx --yes @anthropic-ai/claude-code
```

Then type `/plan-diet` plus your request.

---

## Always-on files (used across many steps)

These are not one step. They sit in the background.

| Role | File called |
|------|-------------|
| Project rules the manager must follow | `CLAUDE.md` |
| Hook wiring (when scripts run) | `.claude/settings.json` |
| After almost every file write: update progress | `.claude/hooks/post-write-state.py` |
| Progress memory | `runs/<run-id>/workflow-state.json` |
| Nutrition database server | `.mcp.json` → `mcp/nutrition_server.py` + `mcp/glycemic_index.json` |
| Optional USDA key | `.env` (never commit this) |

After each cook writes their paper, the manager also loads:

| Role | File called |
|------|-------------|
| Check headings, sources, disclaimer | `.claude/skills/artifact-validator/SKILL.md` |

---

## Step 0 — You type the command

You talk to Claude Code. You do not run Python yourself for the workflow.

**Files called**

| Role | File |
|------|------|
| Slash command (the `/plan-diet` recipe) | `.claude/commands/plan-diet.md` |

What happens: that file says “do not invent meals yourself; start the manager.” Your words after `/plan-diet` are `$ARGUMENTS`.

---

## Step 1 — Manager wakes up

**Files called**

| Role | File |
|------|------|
| Coordinator (manager) instructions | `.claude/agents/coordinator.md` |
| Rules | `CLAUDE.md` |

**Files written**

| Role | File |
|------|------|
| Run folder | `runs/<run-id>/` |
| Your request, saved | `runs/<run-id>/input.md` |
| Empty/starting progress | `runs/<run-id>/workflow-state.json` |

The manager writes **no meals**. It only organizes work.

---

## Step 2 — Ask and confirm missing facts

The manager asks you anything still missing: diabetes type, meds, carb/calorie target, allergies, cooking time, budget, activity, hypo history.

**Files called**

| Role | File |
|------|------|
| Intake field list | `CLAUDE.md` (section “Intake fields”) |
| Manager | `.claude/agents/coordinator.md` |

No domain cook runs until you confirm.

---

## Step 3 — Write the requirements paper

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/requirements-formalizer.md` |
| Structure check | `.claude/skills/artifact-validator/SKILL.md` |
| Progress update | `.claude/hooks/post-write-state.py` |

**Files written**

| Role | File |
|------|------|
| Confirmed profile | `runs/<run-id>/artifacts/requirements.md` |

This file also sets flags:

- `needs_glucose_timing` — later timing cook, or skip
- `needs_budget` — later budget cook, or skip

---

## Step 4 — Research (two cooks at the same time)

These two do not wait for each other.

### 4a. Guideline researcher

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/guideline-researcher.md` |
| Web search | Claude Code `WebSearch` / `WebFetch` tools |
| Check + progress | `artifact-validator` skill + `post-write-state.py` |

**Files written**

| Role | File |
|------|------|
| Public guidance with URLs | `runs/<run-id>/artifacts/guidelines.md` |

### 4b. Nutrition lookup

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/nutrition-lookup.md` |
| MCP config | `.mcp.json` |
| MCP server | `mcp/nutrition_server.py` |
| Offline GI table | `mcp/glycemic_index.json` |
| Check + progress | `artifact-validator` skill + `post-write-state.py` |

**Files written**

| Role | File |
|------|------|
| Food carbs / GI table | `runs/<run-id>/artifacts/food-data.md` |

---

## Step 5 — Meal planner

Waits until Step 3 and Step 4 papers exist.

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/meal-planner.md` |
| Reads | `requirements.md`, `guidelines.md`, `food-data.md` |
| Check + progress | `artifact-validator` skill + `post-write-state.py` |

**Files written**

| Role | File |
|------|------|
| 7-day meals with carbs | `runs/<run-id>/artifacts/meal-plan.md` |

---

## Step 6 — Recipes, groceries, and maybe timing (parallel)

All of these wait for the meal plan. They can run at the same time.

### 6a. Recipe nutritionist

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/recipe-nutritionist.md` |
| Reads | `meal-plan.md`, `food-data.md`, `requirements.md` |
| Web search | `WebSearch` / `WebFetch` |

**Files written**

| Role | File |
|------|------|
| Recipes | `runs/<run-id>/artifacts/recipes.md` |

### 6b. Grocery planner

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/grocery-planner.md` |
| Reads | `meal-plan.md`, `recipes.md` (if already there), `food-data.md`, `requirements.md` |

**Files written**

| Role | File |
|------|------|
| Shopping list | `runs/<run-id>/artifacts/grocery-list.md` |

### 6c. Glucose timing (only sometimes)

**Runs only if** `needs_glucose_timing: true` in `requirements.md` (insulin, sulfonylureas, or hypo history).

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/glucose-timing-advisor.md` |
| Reads | `requirements.md`, `guidelines.md`, `meal-plan.md` |
| Web search | `WebSearch` / `WebFetch` |

**Files written**

| Role | File |
|------|------|
| Meal timing + 15 g rescue carbs | `runs/<run-id>/artifacts/timing.md` |

If skipped, this file is **not** created. Example: vegetarian metformin run skips it; type 1 athlete sample keeps it.

---

## Step 7 — Budget (only sometimes)

**Runs only if** `needs_budget: true` (you gave a dollar cap). Waits for the grocery list.

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/budget-aggregator.md` |
| Reads | `grocery-list.md`, `requirements.md` |
| Web search | price pages via `WebSearch` / `WebFetch` |

**Files written**

| Role | File |
|------|------|
| Cost rollup vs cap | `runs/<run-id>/artifacts/budget.md` |

---

## Step 8 — Validator (the teacher)

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/validator.md` |
| Gate list | `CLAUDE.md` (Quality gates) |
| Structure skill | `.claude/skills/artifact-validator/SKILL.md` |
| Reads | every artifact listed in `workflow-state.json` except the HTML |

**Files written**

| Role | File |
|------|------|
| Pass/fail report | `runs/<run-id>/artifacts/validation.md` |

If a gate fails: manager re-runs **only** the owning agent and downstream papers, max **3** retries. Then validator again. If still failing, the run stops (`status: blocked`). No weekly plan, no HTML.

---

## Step 9 — Weekly plan (one human-readable document)

Runs only after validator **passes**.

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/weekly-plan-builder.md` |
| Reads | all validated artifacts (and `approval.md` comments if this is a revision) |

**Files written**

| Role | File |
|------|------|
| Combined week | `runs/<run-id>/artifacts/weekly-plan.md` |

This is what you read to say yes or no. Not the HTML yet.

---

## Step 10 — You approve or reject

**Files called**

| Role | File |
|------|------|
| Manager | `.claude/agents/coordinator.md` |
| Approval lock | `.claude/hooks/approval-gate-guard.py` |

**Files written**

| Role | File |
|------|------|
| Your decision | `runs/<run-id>/approval.md` |

Put exactly:

```text
status: pending     # waiting for you
status: rejected    # fix and ask again → back to weekly-plan-builder
status: approved    # only then HTML is allowed
```

---

## Step 11 — HTML guide (final output)

**Files called**

| Role | File |
|------|------|
| Agent | `.claude/agents/html-builder.md` |
| Theme / how it should look | `.claude/skills/diet-html-theme-builder/SKILL.md` |
| HTML template | `.claude/skills/diet-html-theme-builder/template.html` |
| Reads | `weekly-plan.md` and `approval.md` |
| Block HTML if not approved | `.claude/hooks/approval-gate-guard.py` |
| Block HTML if it leaks internal names | `.claude/hooks/no-leak-guard.py` |

**Files written**

| Role | File |
|------|------|
| Browser guide | `runs/<run-id>/diet-guide.html` |

Open that file in a browser. That is the app output.

---

## Picture of the file flow

```text
.claude/commands/plan-diet.md
        ↓
.claude/agents/coordinator.md
        ↓
requirements.md
        ↓
guidelines.md  +  food-data.md     (same time)
        ↓
meal-plan.md
        ↓
recipes.md  +  grocery-list.md  +  timing.md?     (same time)
        ↓
budget.md? 
        ↓
validation.md
        ↓
weekly-plan.md
        ↓
approval.md   ← you type approved / rejected
        ↓
diet-guide.html
```

`?` means that cook may be skipped.

---

## Resume (if you stop in the middle)

Run `/plan-diet` again and name the same `<run-id>`.

**Files called**

| Role | File |
|------|------|
| Command | `.claude/commands/plan-diet.md` |
| Manager | `.claude/agents/coordinator.md` |
| Memory | `runs/<run-id>/workflow-state.json` |

Completed cooks in `completed` are not redone unless a failed gate or a rejection says they must be.

---

## Sample runs already in the repo

| Folder | What it shows |
|--------|----------------|
| `runs/01-type2-vegetarian/` | Budget cook on, timing cook off |
| `runs/02-type1-athlete/` | Timing cook on, budget cook off |
| `runs/03-type2-limited-cooking/` | Budget + sodium, timing off |

Each sample has `input.md`, `artifacts/`, `workflow-state.json`, `approval.md`, and `diet-guide.html`.
