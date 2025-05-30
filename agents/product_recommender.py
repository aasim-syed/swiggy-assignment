import json

def recommend_product(context):
    prefs = context.get("preferences", {})
    with open("product_db/mock_products.json") as f:
        products = json.load(f)
    
    matches = [
        p for p in products
        if p["brand"].lower() == prefs["brand"].lower()
        and prefs["color"].lower() in p["name"].lower()
    ]
    context["recommendations"] = matches[:3]
    return context
