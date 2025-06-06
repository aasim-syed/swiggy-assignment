import os
from difflib import SequenceMatcher

def find_similar_products(context):
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

    recommendations = context.get("recommendations", [])
    all_products = context.get("all_products", recommendations)

    if not recommendations or not all_products:
        context["error"] = "No base products to search similar from."
        return context

    try:
        # Automatically select the first product
        selected_product = recommendations[0].get("name", "").lower()

        similar = []
        for p in all_products:
            name = p.get("name", "").lower()
            score = SequenceMatcher(None, selected_product, name).ratio()
            if selected_product in name or score > 0.6:
                similar.append(p)

        # Update recommendations with top 5 similar products
        context["recommendations"] = similar[:5]

        # Ask for confirmation only after showing similar products
        print("\n🔁 Based on your interest in:", selected_product.title())
        print("Here are some similar items we found:")
        for i, prod in enumerate(context["recommendations"], 1):
            print(f"{i}. {prod.get('name')} - ₹{prod.get('price', 'N/A')}")

        if not mock_mode:
            print("\n🧐 Are these the kind of products you were looking for? (yes/no)")
            user_feedback = input("> ").strip().lower()
            context["similar_products_confirmed"] = user_feedback in ["yes", "y"]
        else:
            context["similar_products_confirmed"] = True  # auto confirm in mock

    except Exception as e:
        context["error"] = f"Finding similar products failed: {str(e)}"

    return context
