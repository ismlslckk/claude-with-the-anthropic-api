# Input

## Raw request

```text
/plan-diet Plan a 7-day vegetarian diet for newly diagnosed type 2 diabetes. I am 54,
take metformin 500 mg twice daily, no insulin, no hypoglycemia history. Target about
1700 kcal and 130-160 g carbohydrate per day. Peanut allergy only. Mediterranean-style,
35-minute cooking, household of 1, grocery budget $80/week, walking 30 minutes most days.
```

## Confirmed intake

| Field | Value | Source |
|-------|-------|--------|
| Diabetes type | Type 2, newly diagnosed | user request |
| Age | 54 | user request |
| Medications | Metformin 500 mg twice daily. No insulin, no sulfonylureas. | user request |
| Hypoglycemia history | None | user request |
| Calorie target | ~1700 kcal/day | user request |
| Carb target | 130-160 g/day | user request |
| Allergies / intolerances | Peanut only. Tree nuts, gluten, lactose, soy all allowed. | confirmed 2026-08-19 |
| Diet scope | Lacto-ovo vegetarian (dairy + eggs; no meat, no fish) | confirmed 2026-08-19 |
| Eating pattern | 3 meals + 1 snack per day | confirmed 2026-08-19 |
| Cooking time | 35 minutes | user request |
| Cuisine / preferences | Mediterranean-style | user request |
| Household size | 1 | user request |
| Grocery budget | $80 / week | user request |
| Activity | Walking 30 minutes most days | user request |

## Workflow flags

- `needs_glucose_timing: false` — no insulin, no sulfonylureas, no hypoglycemia history.
- `needs_budget: true` — numeric cap of $80/week confirmed.

## Disclaimer

Educational output only. Not medical advice. Does not diagnose, prescribe, or change
medications. A clinician or registered dietitian must review before real-world use.
