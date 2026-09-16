# Glucose timing

## Metadata
- agent: glucose-timing-advisor
- run_id: 02-type1-athlete
- generated_at: 2026-08-18T17:15:00+00:00

## Sources
- [CDC — Low blood sugar (hypoglycemia)](https://www.cdc.gov/diabetes/treatment/low-blood-sugar-hypoglycemia.html)
- [ADA — Fitness](https://diabetes.org/health-wellness/fitness)

## Why this agent ran
Insulin pump plus user-confirmed lows around long runs (`needs_glucose_timing: true`).

## Day timing
Assume a late-afternoon run (~16:30) on days 1–6. Rest morning on day 7.

- Breakfast ~07:30 (include juice on training days)
- Lunch ~12:00
- Pre-run snack ~15:45 (banana + peanut butter, ~35 g carbohydrate)
- Run ~16:30–17:30
- Post-run snack ~17:45 (yogurt + berries; add juice on days 4 and 7 if extra hungry)
- Dinner ~19:00

Do not change pump settings in this workflow. Discuss timing with the user's diabetes care team.

## Rescue carbs
- Item: glucose tablets, 15 g (one and a half 10 g servings, or follow the product label)
- carbs_g: 15
- when to use: symptoms of hypoglycemia as defined by the user's clinician / CDC public 15 g guidance
- source: https://www.cdc.gov/diabetes/treatment/low-blood-sugar-hypoglycemia.html
- Alternate: 250 ml orange juice (~24 g) if tablets are unavailable

Carry tablets on every run. Recheck glucose per the user's care plan — this document does not set insulin doses.

## Disclaimer
Educational timing notes only. Medication changes require a clinician. Not medical advice.
