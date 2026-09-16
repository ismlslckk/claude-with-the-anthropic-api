# Validation

## Metadata
- agent: validator
- run_id: 01-type2-vegetarian
- generated_at: 2026-08-18T15:35:00+00:00

## Result
- passed: true

## Gates
| Gate | Status | Owner agent | Finding |
|------|--------|-------------|---------|
| daily_carbs_in_range | pass | meal-planner | Days 1–7 are 130–147 g (range 130–160) |
| meals_have_carbs_and_source | pass | meal-planner | Every meal lists carbs_g and a source |
| no_allergens | pass | meal-planner | Peanuts absent; almonds confirmed allowed |
| hypo_rescue_if_insulin | n/a | glucose-timing-advisor | needs_glucose_timing is false |
| budget_within_cap | pass | budget-aggregator | 64.80 USD ≤ 80 USD |
| disclaimer_present | pass | requirements-formalizer | Disclaimer on requirements and meal plan |
| eating_pattern_covered | pass | meal-planner | Breakfast, lunch, dinner, snack each day |
| sodium_respected | n/a | meal-planner | No sodium cap confirmed |

## Retry map
None. All applicable gates passed.

## Disclaimer
Educational quality check, not a clinical review. Not medical advice.
