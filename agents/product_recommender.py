import json
import os

def recommend_product(context):
    preferences = context.get("preferences", {})
    brand = preferences.get('brand', 'any').lower()
    color = preferences.get('color', 'any').lower()
    price_range = preferences.get('price_range', '0-10000')

    # Parse price range
    try:
        min_price, max_price = map(int, price_range.split('-'))
    except:
        min_price, max_price = 0, float('inf')

    # Load products from JSON
    json_path = os.path.join(os.path.dirname(__file__), "..", "product_db", "mock_products.json")
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    # Filter recommendations
    recommendations = []
    for product in product_catalog:
        if (brand == "any" or brand in product.get("brand", "").lower()) and \
           (color == "any" or color in product.get("color", "").lower()) and \
           (min_price <= product.get("price", 0) <= max_price):
            recommendations.append(product)

    context["recommendations"] = recommendations
    return context
