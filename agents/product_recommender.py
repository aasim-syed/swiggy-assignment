import json

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

    product_catalog = [
        {"id": 1, "name": "Nike Air Max White", "brand": "Nike", "color": "white", "price": 4500},
        {"id": 2, "name": "Adidas Ultraboost Black", "brand": "Adidas", "color": "black", "price": 5200},
    ]

    recommendations = []
    for product in product_catalog:
        if (brand == "any" or brand in product["brand"].lower()) and \
           (color == "any" or color in product["color"].lower()) and \
           min_price <= product["price"] <= max_price:
            recommendations.append(product)

    context["recommendations"] = recommendations
    return context
