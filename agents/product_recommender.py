import json
import os
from agents.user_clarifier import clarify_preferences
from agents.image_analyzer import analyze_image

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
    except:
        min_price, max_price = 0, float("inf")

    # Load product catalog
    json_path = os.path.join(os.path.dirname(__file__), "..", "product_db", "mock_products.json")
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    def match(product):
        p_brand = product.get("brand", "").lower()
        p_color = product.get("color", "").lower()
        p_price = product.get("price", 0)
        p_category = product.get("category", "").lower()

        return (
            (category in p_category or p_category in category)
            and (brand == "any" or brand in p_brand)
            and (color == "any" or color in p_color)
            and min_price <= p_price <= max_price
        )

    recommendations = [p for p in product_catalog if match(p)]
    context["recommendations"] = recommendations

    if not recommendations:
        print("\n❌ No matching products found.")
        print(f"🔍 DEBUG:\nbrand={brand}, category={category}, color={color}, price_range={min_price}-{max_price}")
        print("Would you like to:")
        print("1. Try again with different preferences")
        print("2. Upload another image")
        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            context["reset_product_type"] = True
            return clarify_preferences(context)
        elif choice == "2":
            context.pop("image_base64", None)
            return analyze_image(context)

    print(f"\n✅ {len(recommendations)} matching products found:")
    for p in recommendations:
        print(f"- {p['name']} | ₹{p['price']} | {p['brand']} | {p['color']}")

    return context
