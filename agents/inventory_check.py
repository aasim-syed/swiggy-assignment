# === File: agents/inventory_check.py ===
import random

def inventory_check(context):
    """
    1. We expect `context["recommendations"]` to be a list of product dicts.
    2. We will simulate a real-time inventory API by randomly flagging some items as 'out_of_stock'.
    3. We update context["inventory_status"] = { product_id: boolean_in_stock }.
    """
    recs = context.get("recommendations", [])
    inventory_status = {}

    # Simulate checking each recommended product against an inventory API
    for prod in recs:
        pid = prod.get("id")
        # Randomly decide in-stock or out-of-stock. In real code, you’d call a proper API.
        in_stock = random.choice([True, True, True, False])  # 75% chance in stock
        inventory_status[pid] = in_stock

    context["inventory_status"] = inventory_status

    # Inform the user which items are out of stock:
    print("\n🔍 Checking real-time inventory availability...")
    for prod in recs:
        pid = prod["id"]
        if not inventory_status[pid]:
            print(f"⚠️  {prod['name']} (ID: {pid}) is currently OUT OF STOCK.")

    # Filter out out-of-stock items automatically
    in_stock_recs = [p for p in recs if inventory_status.get(p["id"], False)]
    context["recommendations"] = in_stock_recs

    if not in_stock_recs:
        print("❌ Sorry, none of the matched products are in stock. Please try again later or refine your preferences.")
    else:
        print(f"✅ {len(in_stock_recs)} item(s) remain in stock.")

    return context
