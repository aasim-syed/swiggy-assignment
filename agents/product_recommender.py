import json
import os
from agents.user_clarifier import clarify_preferences
from agents.image_analyzer import analyze_image

def recommend_product(context):
    preferences = context.get("preferences", {})
    product_type = context.get("product_type", "product").lower()

    brand = preferences.get('brand', 'any').lower()
    color = preferences.get('color', 'any').lower()
    price_range = preferences.get('price_range', '0-10000')

    try:
        min_price, max_price = map(int, price_range.split('-'))
    except:
        min_price, max_price = 0, float('inf')

    # Load mock product catalog
    json_path = os.path.join(os.path.dirname(__file__), "..", "product_db", "mock_products.json")
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    # Match category more flexibly
    def category_matches(p_category, user_type):
        return user_type in p_category.lower() or p_category.lower() in user_type

    recommendations = []
    for product in product_catalog:
        if not category_matches(product.get("category", ""), product_type):
            continue
        if (brand == "any" or brand in product.get("brand", "").lower()) and \
           (color == "any" or color in product.get("color", "").lower()) and \
           (min_price <= product.get("price", 0) <= max_price):
            recommendations.append(product)

    context["recommendations"] = recommendations

    if not recommendations:
        print("\n❌ No matching products found.")
        print("Would you like to:")
        print("1. Try again with different preferences")
        print("2. Upload another image")
        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            return clarify_preferences(context)
        elif choice == "2":
            context.pop("image_base64", None)
            return analyze_image(context)

    return context
