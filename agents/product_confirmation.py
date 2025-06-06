def confirm_product_type(context):
    """
    Confirms the detected product type with the user.
    If incorrect, allows manual correction.
    """
    if context.get("product_type_confirmed", False):
        return context  # Already confirmed

    product_type = context.get("product_type", "unknown")
    mock_mode = context.get("mock", True)

    if mock_mode:
        print(f"🤖 [MOCK] Detected product type: {product_type}")
        context["product_type_confirmed"] = True
        return context

    print(f"\n🤖 We detected your product as '{product_type}'. Is this correct? (yes/no)")
    user_input = input("> ").strip().lower()

    if user_input not in ["yes", "y"]:
        corrected = input("🔍 Please enter the correct product type: ").strip().lower()
        context["product_type"] = corrected

    context["product_type_confirmed"] = True
    return context
