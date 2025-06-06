# === File: agents/confirmation.py ===

def final_check(context):
    """
    1. Expects context["recommendations"] to be a non-empty list of product dicts.
    2. Prints each remaining product with an index (1-based).
    3. Prompts the user to choose one (or type 'refine' to return to clarifier).
    4. Updates context["confirmed_product"] = that product dict (or None if refine).
    """
    recs = context.get("recommendations", [])
    if not recs:
        # Nothing to confirm
        context["confirmed_product"] = None
        return context

    print("\n🎯 Please confirm which of these products you want:")
    for idx, prod in enumerate(recs, start=1):
        print(f"  {idx}. {prod['name']} | {prod['brand']} | ₹{prod['price']} | Color: {prod['color']}")

    choice = None
    while choice is None:
        raw = input("Type 1–{} to confirm, or 'refine' to revisit preferences: ".format(len(recs))).strip().lower()
        if raw == "refine":
            context["confirmed_product"] = None
            return context  # LangGraph will send you back to Clarifier (once we update the graph)
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(recs):
                context["confirmed_product"] = recs[idx - 1]
                choice = recs[idx - 1]
            else:
                print(f"🚫 Please enter a number between 1 and {len(recs)}.")
        else:
            print("🚫 Invalid input. Type a number or 'refine'.")

    print(f"👍 You confirmed: {choice['name']} (ID: {choice['id']}).")
    return context
