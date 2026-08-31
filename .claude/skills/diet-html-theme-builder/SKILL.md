---
name: diet-html-theme-builder
description: HTML rendering rules and the predefined diet-guide template. Use when building diet-guide.html after human approval.
---

# Diet HTML theme builder

Read [template.html](template.html) and fill it from `weekly-plan.md`. Keep the visual system below so repeated runs look consistent.

## Visual system

- Page max-width 880px, centered, background `#f4f7f5`
- Header bar `#0f4c5c`, text white
- Accent `#e36414` for carb chips and the approval stamp
- Disclaimer banner: `#fff3cd` background, `#5c4813` text, 1px `#e2c56b` border — first content after the header
- Cards: white, 12px radius, light shadow, 16px padding
- Day sections: H2 with a left border `#0f4c5c`
- Tables: full width, header row `#0f4c5c` white text
- Footer: small muted text, no internal filenames

## Section order (required)

1. Header (title + run subtitle)
2. Disclaimer banner
3. Profile snapshot
4. How to use this week
5. Daily schedule (7 days)
6. Grocery list
7. Recipes
8. Safety
9. Sources (visible URLs)
10. Footer ("Educational workflow output")

## Leak ban

Do not include: `artifacts/`, `workflow-state.json`, `requirements.md`, `validation.md`, `meal-plan.md`, `food-data.md`, `guidelines.md`, `CLAUDE.md`, agent file paths, or hook names.

## Output

One standalone HTML file with CSS in a `<style>` tag. No external stylesheets, fonts, or scripts.
