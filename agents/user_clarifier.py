def clarify_preferences(context):
    product_type = context.get("product_type", "product")
    questions = [
        f"What brand of {product_type} are you looking for?",
        f"What is your preferred color?",
        f"Do you have a price range in mind?"
    ]
    context["questions"] = questions
    # Assume user responses are simulated or injected
    context["preferences"] = {
        "brand": "Nike", "color": "white", "price_range": "3000-5000"
    }
    return context
