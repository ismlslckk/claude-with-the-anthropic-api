# Diabetes diet workflow

Educational Claude Code workflow. **Not medical advice.** It does not diagnose, prescribe, or change medications. A clinician or registered dietitian must review any real-world use.

## How a run starts

The user invokes `/plan-diet` (`.claude/commands/plan-diet.md`). That command instantiates the `coordinator` subagent. The coordinator produces no diet content. It gathers requirements, writes the execution plan, selects subagents, runs gates, enforces approval, and persists state.

## Hub-and-spoke

```
requirements-formalizer
  → [guideline-researcher, nutrition-lookup]          # parallel
  → meal-planner
  → [recipe-nutritionist, grocery-planner, glucose-timing-advisor?]  # parallel; timing is conditional
  → budget-aggregator?                                # conditional
  → validator                                         # gates; targeted retry, max 3
  → weekly-plan-builder
  → human approval                                    # approval.md; revision loop on reject
  → html-builder                                      # diet-guide.html
```

Independent agents in a stage run in parallel. The next stage waits. The coordinator never regenerates a completed artifact unless a gate retry or an approval rejection requires it.

## Dynamic selection

Read `artifacts/requirements.md` workflow flags:

| Flag | Agent | When |
|------|--------|------|
| `needs_glucose_timing: true` | `glucose-timing-advisor` | Insulin, sulfonylureas, or hypoglycemia history |
| `needs_budget: true` | `budget-aggregator` | Numeric grocery budget was confirmed |

All other listed agents always run.

## Artifact ownership

| Agent | Artifact |
|-------|----------|
| requirements-formalizer | `runs/<id>/artifacts/requirements.md` |
| guideline-researcher | `runs/<id>/artifacts/guidelines.md` |
| nutrition-lookup | `runs/<id>/artifacts/food-data.md` |
| meal-planner | `runs/<id>/artifacts/meal-plan.md` |
| recipe-nutritionist | `runs/<id>/artifacts/recipes.md` |
| grocery-planner | `runs/<id>/artifacts/grocery-list.md` |
| glucose-timing-advisor | `runs/<id>/artifacts/timing.md` |
| budget-aggregator | `runs/<id>/artifacts/budget.md` |
| validator | `runs/<id>/artifacts/validation.md` |
| weekly-plan-builder | `runs/<id>/artifacts/weekly-plan.md` |
| html-builder | `runs/<id>/diet-guide.html` |

Each Markdown artifact must include `## Metadata`, `## Sources`, and `## Disclaimer` (see the `artifact-validator` skill). Agents do not edit files they do not own.

## External knowledge

Do not rely on model memory for nutrient numbers or clinical guidance.

- `guideline-researcher` and `recipe-nutritionist` (and `glucose-timing-advisor` / `budget-aggregator` when selected) **must** use WebSearch.
- `nutrition-lookup` **must** use the `nutrition` MCP (`search_foods`, `get_nutrition`, `lookup_glycemic_index`; `search_usda` if `USDA_API_KEY` is set).

## Skills

- `artifact-validator` — structural + citation check after each new artifact, before dependent work.
- `diet-html-theme-builder` — HTML theme and template for the approved guide.

## Hooks

Configured in `.claude/settings.json`:

- **PreToolUse** `approval-gate-guard.py` — blocks `diet-guide.html` until `approval.md` contains `status: approved`.
- **PreToolUse** `no-leak-guard.py` — blocks `diet-guide.html` if internal artifact filenames appear.
- **PostToolUse** `post-write-state.py` — updates `workflow-state.json` when run files are written.

## Quality gates

`validator` scores these gates (skip with `n/a` when the flag is false):

1. `daily_carbs_in_range`
2. `meals_have_carbs_and_source`
3. `no_allergens`
4. `hypo_rescue_if_insulin`
5. `budget_within_cap`
6. `disclaimer_present`
7. `eating_pattern_covered`
8. `sodium_respected`

On failure, re-run **only** the owning agent and any downstream artifacts that consume it. Max **3** retries per agent. Unresolved failures set `status: blocked` and stop the run. Downstream work must not proceed.

Gate → owner mapping:

| Gate | Owner | Downstream to regenerate |
|------|--------|--------------------------|
| daily_carbs_in_range | meal-planner | recipes, grocery, timing?, budget?, weekly-plan |
| meals_have_carbs_and_source | meal-planner | recipes, weekly-plan |
| no_allergens | meal-planner (and recipe-nutritionist if recipes already exist) | recipes, grocery, weekly-plan |
| hypo_rescue_if_insulin | glucose-timing-advisor | weekly-plan |
| budget_within_cap | budget-aggregator (then meal-planner if swaps needed) | grocery, weekly-plan |
| disclaimer_present | the artifact missing it | dependents of that artifact |
| eating_pattern_covered | meal-planner | recipes, grocery, weekly-plan |
| sodium_respected | meal-planner | recipes, grocery, weekly-plan |

## Human approval

After `weekly-plan.md`:

1. Write `runs/<id>/approval.md` with `status: pending`.
2. Ask the user to approve or reject with comments.
3. Reject → `status: rejected`, revise via `weekly-plan-builder` (and upstream if needed), request approval again.
4. Approve → `approval.md` must contain the exact line `status: approved` (deterministic hook check).
5. Only then run `html-builder`.

## Persistence and resume

State file: `runs/<id>/workflow-state.json`.

On `/plan-diet` with an existing run (user names the run id, or the coordinator finds an incomplete run):

- Do not redo `completed` agents unless a retry or rejection invalidates them.
- Continue the first incomplete stage.
- Preserve artifacts already on disk.

## Intake fields

Confirm before `requirements-formalizer`: diabetes type, medications, kcal or carb target (or permission to propose), allergies, eating pattern, cooking time, cuisine/preferences, grocery budget or `none`, activity, hypoglycemia history.

## Final output

Human-readable `diet-guide.html` (Markdown weekly plan is the approval surface). Structure must stay stable across repeated runs with the same input.
