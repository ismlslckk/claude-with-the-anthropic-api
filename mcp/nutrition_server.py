#!/usr/bin/env python3
"""Nutrition MCP server for the diabetes diet workflow.

Reuses the FastMCP pattern from anthropic-api-course/cli_project/mcp_server.py.
Looks up foods via Open Food Facts (no key), an optional USDA FoodData Central
key, and a local glycemic-index table that works offline.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import Field

try:
    import certifi
    import ssl

    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL_CTX = None

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / ".env")

mcp = FastMCP("NutritionMCP", log_level="ERROR")

GI_PATH = ROOT / "glycemic_index.json"
OFF_SEARCH = "https://world.openfoodfacts.org/cgi/search.pl"
OFF_PRODUCT = "https://world.openfoodfacts.org/api/v2/product/{code}.json"
USDA_SEARCH = "https://api.nal.usda.gov/fdc/v1/foods/search"
USER_AGENT = "diabetes-diet-workflow/0.1 (educational MCP)"
TIMEOUT_S = 12


def _http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S, context=_SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _load_gi() -> dict:
    return json.loads(GI_PATH.read_text(encoding="utf-8"))


def _nutrients_from_off(product: dict) -> dict:
    n = product.get("nutriments") or {}

    def num(key: str):
        value = n.get(key)
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    return {
        "source": "Open Food Facts",
        "source_url": product.get("url") or f"https://world.openfoodfacts.org/product/{product.get('code', '')}",
        "name": product.get("product_name") or product.get("generic_name") or "unknown",
        "brands": product.get("brands"),
        "code": product.get("code"),
        "per": "100g",
        "energy_kcal": num("energy-kcal_100g") or num("energy-kcal"),
        "carbohydrates_g": num("carbohydrates_100g"),
        "sugars_g": num("sugars_100g"),
        "fiber_g": num("fiber_100g"),
        "protein_g": num("proteins_100g"),
        "fat_g": num("fat_100g"),
        "salt_g": num("salt_100g"),
        "sodium_mg": (num("sodium_100g") * 1000) if num("sodium_100g") is not None else None,
    }


@mcp.tool(
    name="lookup_glycemic_index",
    description="Look up glycemic index and glycemic load from the local educational GI table. Works offline.",
)
def lookup_glycemic_index(
    query: str = Field(description="Food name to match, e.g. 'lentils' or 'oats'"),
    limit: int = Field(default=8, description="Maximum matches to return"),
) -> dict:
    data = _load_gi()
    q = query.strip().lower()
    foods = data.get("foods", [])
    matches = [f for f in foods if q in f["name"] or f["name"] in q]
    if not matches:
        matches = [f for f in foods if any(part and part in f["name"] for part in q.split())]
    return {
        "disclaimer": data.get("disclaimer"),
        "source": data.get("source"),
        "query": query,
        "matches": matches[: max(1, min(limit, 25))],
    }


@mcp.resource("nutrition://glycemic-index", mime_type="application/json")
def glycemic_index_resource() -> str:
    return GI_PATH.read_text(encoding="utf-8")


@mcp.tool(
    name="search_foods",
    description="Search Open Food Facts for packaged foods. Returns name, barcode, brands, and a product page URL. No API key required.",
)
def search_foods(
    query: str = Field(description="Search terms such as 'plain greek yogurt' or 'canned black beans'"),
    page_size: int = Field(default=5, description="Number of products to return (1-15)"),
) -> dict:
    page_size = max(1, min(int(page_size), 15))
    params = urllib.parse.urlencode(
        {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": page_size,
        }
    )
    try:
        payload = _http_get_json(f"{OFF_SEARCH}?{params}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": f"Open Food Facts search failed: {exc}", "query": query}

    products = []
    for item in payload.get("products", [])[:page_size]:
        code = item.get("code")
        products.append(
            {
                "name": item.get("product_name") or item.get("generic_name") or "unknown",
                "brands": item.get("brands"),
                "code": code,
                "url": item.get("url") or (f"https://world.openfoodfacts.org/product/{code}" if code else None),
                "quantity": item.get("quantity"),
            }
        )
    return {"ok": True, "source": "Open Food Facts", "query": query, "count": len(products), "products": products}


@mcp.tool(
    name="get_nutrition",
    description="Get per-100g macros from Open Food Facts by barcode, or by name (uses the first search hit).",
)
def get_nutrition(
    query: str = Field(description="Barcode (digits) or food name"),
) -> dict:
    q = query.strip()
    try:
        if q.isdigit():
            payload = _http_get_json(OFF_PRODUCT.format(code=q))
            product = payload.get("product")
            if not product:
                return {"ok": False, "error": "Product not found", "query": query}
            return {"ok": True, **_nutrients_from_off(product)}

        search = search_foods(query=q, page_size=1)
        if not search.get("ok") or not search.get("products"):
            return {"ok": False, "error": "No Open Food Facts match", "query": query, "search": search}
        code = search["products"][0].get("code")
        if not code:
            return {"ok": False, "error": "Match had no barcode", "query": query}
        payload = _http_get_json(OFF_PRODUCT.format(code=code))
        product = payload.get("product")
        if not product:
            return {"ok": False, "error": "Product details not found", "query": query}
        return {"ok": True, **_nutrients_from_off(product)}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": f"Open Food Facts lookup failed: {exc}", "query": query}


@mcp.tool(
    name="search_usda",
    description="Search USDA FoodData Central. Requires USDA_API_KEY in the environment. Skip if the key is unset.",
)
def search_usda(
    query: str = Field(description="Food search query"),
    page_size: int = Field(default=5, description="Number of foods to return (1-15)"),
) -> dict:
    api_key = os.getenv("USDA_API_KEY", "").strip()
    if not api_key:
        return {
            "ok": False,
            "error": "USDA_API_KEY is not set. Use search_foods / get_nutrition / lookup_glycemic_index instead.",
            "query": query,
        }
    page_size = max(1, min(int(page_size), 15))
    params = urllib.parse.urlencode({"query": query, "pageSize": page_size, "api_key": api_key})
    try:
        payload = _http_get_json(f"{USDA_SEARCH}?{params}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": f"USDA search failed: {exc}", "query": query}

    foods = []
    for item in payload.get("foods", [])[:page_size]:
        nutrients = {n.get("nutrientName"): n.get("value") for n in item.get("foodNutrients") or []}
        foods.append(
            {
                "fdc_id": item.get("fdcId"),
                "description": item.get("description"),
                "data_type": item.get("dataType"),
                "brand": item.get("brandOwner"),
                "source_url": f"https://fdc.nal.usda.gov/food-details/{item.get('fdcId')}/nutrients",
                "energy_kcal": nutrients.get("Energy"),
                "carbohydrates_g": nutrients.get("Carbohydrate, by difference"),
                "fiber_g": nutrients.get("Fiber, total dietary"),
                "protein_g": nutrients.get("Protein"),
                "fat_g": nutrients.get("Total lipid (fat)"),
                "sodium_mg": nutrients.get("Sodium, Na"),
            }
        )
    return {"ok": True, "source": "USDA FoodData Central", "query": query, "count": len(foods), "foods": foods}


if __name__ == "__main__":
    mcp.run(transport="stdio")
