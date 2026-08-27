# Nutrition MCP

Custom FastMCP server used by the diabetes diet workflow. Pattern follows the archived course server in `anthropic-api-course/cli_project/mcp_server.py`.

## Tools

- `search_foods` — Open Food Facts product search (no API key)
- `get_nutrition` — macros for a barcode or food name
- `lookup_glycemic_index` — local GI/GL table (offline)
- `search_usda` — USDA FoodData Central (requires `USDA_API_KEY`)

## Run locally

```bash
uv run --directory mcp python nutrition_server.py
```
