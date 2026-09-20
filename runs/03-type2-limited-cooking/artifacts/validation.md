# Validation

## Metadata
- agent: validator
- run_id: 03-type2-limited-cooking
- generated_at: 2026-08-18T19:45:00+00:00

## Result
- passed: true

## Gates
| Gate | Status | Owner agent | Finding |
|------|--------|-------------|---------|
| daily_carbs_in_range | pass | meal-planner | Days 1–7 are 121–135 g (range 120–150) |
| meals_have_carbs_and_source | pass | meal-planner | Every meal lists carbs_g and a source |
| no_allergens | pass | meal-planner | No confirmed allergens |
| hypo_rescue_if_insulin | n/a | glucose-timing-advisor | needs_glucose_timing is false |
| budget_within_cap | pass | budget-aggregator | 37.50 USD ≤ 50 USD |
| disclaimer_present | pass | requirements-formalizer | Present on requirements and meal plan |
| eating_pattern_covered | pass | meal-planner | Breakfast, lunch, dinner each day |
| sodium_respected | pass | meal-planner | No-salt beans, no broth cubes, FDA sodium page cited |

## Retry map
None. All applicable gates passed.

## Disclaimer
Educational quality check, not a clinical review. Not medical advice.
