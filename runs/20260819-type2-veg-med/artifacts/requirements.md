# Requirements

## Metadata
- agent: requirements-formalizer
- run_id: 20260819-type2-veg-med
- generated_at: 2026-08-19T00:00:00Z
- status: complete
- input_source: runs/20260819-type2-veg-med/input.md (intake confirmed 2026-08-19)

## Profile
- diabetes_type: Type 2, newly diagnosed
- medications: Metformin 500 mg twice daily. No insulin. No sulfonylureas.
- hypoglycemia_history: None
- age_or_life_stage: 54 years old, adult
- activity_level: Walking 30 minutes most days (light to moderate)
- eating_pattern: 3 meals + 1 snack per day = 4 eating occasions every day, all 7 days

## Nutrition targets
- kcal_per_day: ~1700 kcal/day
- carb_g_per_day: 130-160 g/day (range used by the `daily_carbs_in_range` gate; each day must land inside this range)
- protein_notes: Protein must come from lacto-ovo vegetarian sources only — dairy, eggs, legumes/pulses, whole grains, seeds, tree nuts (peanut excluded). No specific gram target was confirmed by the user; do not assert one.
- sodium_limit: Target < 2300 mg sodium/day. Rationale: general population / cardiometabolic upper-intake target commonly applied in diabetes nutrition guidance, used here so the `sodium_respected` gate is objectively checkable. This is a general population target, not a prescription for this user, and was not confirmed by the user. Label as `proposed, awaiting confirmation`.
- other_limits: None confirmed beyond the calorie, carbohydrate, and sodium targets above. No potassium, phosphorus, fluid, alcohol, or saturated-fat limit was confirmed.

## Constraints
- allergies_intolerances: Peanut only — strict exclusion of peanuts, peanut butter, peanut oil, and peanut-containing products. Tree nuts, gluten, lactose/dairy, and soy are all explicitly permitted.
- diet_pattern: Lacto-ovo vegetarian — dairy and eggs included; no meat, no poultry, no fish, no seafood (also excludes fish sauce, anchovy, gelatin-style animal ingredients and meat/fish broths)
- cuisine_preferences: Mediterranean-style
- cooking_time_minutes: 35 maximum per recipe
- household_size: 1
- grocery_budget: $80 per week — hard cap

## Workflow flags
- needs_glucose_timing: false
- needs_budget: true

Reasoning for flags (from confirmed intake only): no insulin, no sulfonylureas, and no hypoglycemia history, so glucose-timing work is not triggered. A numeric weekly grocery cap of $80 was confirmed, so budget aggregation is required.

## Confirmed request
Plan a 7-day vegetarian diet for newly diagnosed type 2 diabetes. User is 54, takes
metformin 500 mg twice daily, no insulin, no hypoglycemia history. Target about
1700 kcal and 130-160 g carbohydrate per day. Peanut allergy only. Mediterranean-style,
35-minute cooking, household of 1, grocery budget $80/week, walking 30 minutes most days.

Additional items confirmed at intake on 2026-08-19: allergy scope is peanut only (tree nuts,
gluten, lactose, and soy all allowed); diet scope is lacto-ovo vegetarian (dairy and eggs
included, no meat and no fish); eating pattern is 3 meals plus 1 snack per day.

## Sources
- User-confirmed intake: `runs/20260819-type2-veg-med/input.md`, confirmed 2026-08-19 (no external medical diagnosis)
- No external clinical guideline citations are made in this artifact. Guideline sourcing is the `guideline-researcher`'s responsibility.

## Disclaimer
Educational meal-planning workflow only. Not medical advice, not a substitute for a registered dietitian or clinician. This document does not diagnose, prescribe, or change medications. A clinician or registered dietitian must review before real-world use.
