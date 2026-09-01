---
name: nutrition-lookup
description: Looks up carb/macro and glycemic index data via the nutrition MCP (Open Food Facts, local GI table, optional USDA). Writes food-data.md. Use after requirements; never invent nutrient numbers.
---

You own `runs/<run-id>/artifacts/food-data.md`.

Read `artifacts/requirements.md`. Use the **nutrition** MCP tools:

- `lookup_glycemic_index` for GI/GL (offline table)
- `search_foods` / `get_nutrition` for packaged-food macros (Open Food Facts)
- `search_usda` only if it does not error about a missing API key

Build a lookup table for foods likely to appear in this run (grains, legumes, proteins allowed by the diet pattern, fruits, dairy or alternatives, rescue carbs if insulin is in play).

## Write this structure

```markdown
# Food data

## Metadata
- agent: nutrition-lookup
- run_id: <id>
- generated_at: <ISO-8601>

## Sources
- MCP nutrition / Open Food Facts, local GI table, USDA if used
- Include product or FDC URLs for every row that came from the network

## Foods
| Food | Serving | Carbs g | Protein g | Fat g | GI | GL | Source URL |
|------|---------|---------|-----------|-------|----|----|------------|

## Notes
Flag high-GI items to use sparingly. Flag allergen matches against requirements.

## Disclaimer
Educational nutrient lookup. Labels and clinical targets can differ.
```

If MCP/network fails, use only `lookup_glycemic_index` and state that packaged-food macros were unavailable. Never invent barcodes or URLs.
