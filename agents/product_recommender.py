import json
import os

def recommend_product(context):
    preferences = context.get("preferences", {})
    product_type = context.get("product_type", "product").lower()

    brand = preferences.get("brand", "any").lower()
    color = preferences.get("color", "any").lower()
    price_range = preferences.get("price_range", "0-100000").strip()
    category = preferences.get("category", "").lower() or product_type

    try:
        if "-" in price_range:
            min_price, max_price = map(int, price_range.split("-"))
        else:
            min_price = 0
            max_price = int(price_range)
    except Exception:
        min_price, max_price = 0, float("inf")

    # Load product catalog
    json_path = os.path.join(os.path.dirname(__file__), "..", "product_db", "mock_products.json")
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    def match(product):
        if "category" not in product or not product["category"]:
            return False

        p_brand = product.get("brand", "").lower()
        p_color = product.get("color", "").lower()
        p_price = product.get("price", 0)
        p_category_raw = product.get("category", "")
        p_categories = [c.strip().lower() for c in p_category_raw.split(",")]

        brand_match = (brand == "any" or brand in p_brand)
        color_match = (color == "any" or color in p_color)
        category_match = category in p_categories
        price_match = min_price <= p_price <= max_price

        # ✅ All must match strictly
        return brand_match and color_match and category_match and price_match

    recommendations = [p for p in product_catalog if match(p)]

    context["recommendations"] = recommendations

    if not recommendations:
        context["error"] = "No matching products found."
        context["debug"] = {
            "brand": brand,
            "category": category,
            "color": color,
            "price_range": f"{min_price}-{max_price}"
        }

    return context
