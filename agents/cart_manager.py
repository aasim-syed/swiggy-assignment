# === File: agents/cart_manager.py ===

def cart_manager(context):
    """
    1. If context["confirmed_product"] is not None, add it to context["cart"] (a list).
    2. Ask the user: "Do you want to add another item? (yes/no)".
    3. If yes, set context["add_more"] = True. If no, set it to False.
    4. Return context so that graph can loop back appropriately.
    """
    # Initialize cart on first run
    if "cart" not in context:
        context["cart"] = []

    confirmed = context.get("confirmed_product")
    if confirmed:
        context["cart"].append(confirmed)
        print(f"\n🛒 Added to cart: {confirmed['name']} (₹{confirmed['price']})")

    # Ask if user wants more items
    while True:
        ans = input("Would you like to add another item? (yes/no): ").strip().lower()
        if ans in ["yes", "y"]:
            context["add_more"] = True
            break
        if ans in ["no", "n"]:
            context["add_more"] = False
            break
        print("🚫 Please type 'yes' or 'no'.")

    return context
