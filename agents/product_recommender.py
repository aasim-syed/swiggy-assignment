# === File: agents/product_recommender.py ===

import json
import os
import difflib
from agents.user_clarifier import clarify_preferences
from agents.image_analyzer import analyze_image
from difflib import SequenceMatcher

def fuzzy_match(a: str, b: str, threshold: float = 0.6) -> bool:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

def recommend_product(context):
    """
    1. Fuzzy‐match against the catalog using difflib for brand/category/color.
    2. If no matches, let user retry or re‐upload.
    3. If matches found, show them and optionally get an LLM‐based rationale.
    4. Ask the user to confirm which product is correct (confirmation step).
    5. If the user rejects, allow adjusting preferences or restarting.
    """
    # If user chose to reset preferences, clear and re‐ask
    if context.get("reset_preferences"):
        context.pop("reset_preferences", None)
        context["preferences"] = {}
        return clarify_preferences(context)

    # Retrieve preferences and product_type
    preferences = context.get("preferences", {})
    product_type = context.get("product_type", "product").lower()

    # Normalize preference fields
    brand = preferences.get("brand", "any")
    brand = brand.lower() if isinstance(brand, str) else "any"

    color = preferences.get("color", "any")
    color = color.lower() if isinstance(color, str) else "any"

    raw_price = preferences.get("price_range", "0-100000")
    if isinstance(raw_price, (list, tuple)) and len(raw_price) == 2:
        min_price, max_price = raw_price
    else:
        raw_price = str(raw_price).strip()
        try:
            if "-" in raw_price:
                low, high = raw_price.split("-")
                min_price, max_price = int(low), int(high)
            else:
                min_price, max_price = 0, int(raw_price)
        except:
            min_price, max_price = 0, float("inf")

    category = preferences.get("category", "").strip().lower() or product_type

    # Load the mock product catalog
    json_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "product_db",
        "mock_products.json"
    )
    with open(json_path, "r") as f:
        product_catalog = json.load(f)

    # Helper for fuzzy string matching
    def is_similar(a: str, b: str, threshold: float = 0.75) -> bool:
        if not a or not b:
            return False
        ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        return ratio >= threshold

    # Return True if product matches all criteria
    def match(product: dict) -> bool:
        p_brand = product.get("brand", "").lower()
        p_color = product.get("color", "").lower()
        p_price = product.get("price", 0)
        p_category = product.get("category", "").lower()
        p_name = product.get("name", "").lower()

        cat_ok = (
            (category in p_category)
            or (p_category in category)
            or is_similar(category, p_category)
            or (category in p_name)
        )
        brand_ok = (
            True if brand == "any"
            else (brand in p_brand)
                 or (p_brand in brand)
                 or is_similar(brand, p_brand)
                 or (brand in p_name)
        )
        color_ok = (
            True if color == "any"
            else (color in p_color)
                 or (p_color in color)
                 or is_similar(color, p_color)
                 or (color in p_name)
        )
        price_ok = (min_price <= p_price <= max_price)

        return cat_ok and brand_ok and color_ok and price_ok

    # Filter all products matching the criteria
    recommendations = [p for p in product_catalog if match(p)]
    context["recommendations"] = recommendations

    # 1. If no matches, prompt user to retry or re-upload
    if not recommendations:
        print("\n❌ No matching products found.")
        print(f"🔍 DEBUG:\n"
              f"  • brand = {brand!r}\n"
              f"  • category = {category!r}\n"
              f"  • color = {color!r}\n"
              f"  • price_range = {min_price}-{max_price}")
        print("Would you like to:")
        print("1. Try again with different preferences")
        print("2. Upload another image")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            context["reset_preferences"] = True
            return recommend_product(context)
        elif choice == "2":
            context.pop("image_base64", None)
            return analyze_image(context)
        else:
            print("⚠️ Invalid choice. Exiting recommendation.")
            return context

    # 2. Display raw matches
    print(f"\n✅ {len(recommendations)} matching product(s) found:")
    for idx, p in enumerate(recommendations, start=1):
        print(f"  {idx}. {p['name']} | ₹{p['price']} | {p['brand']} | {p['color']}")

    # 3. If an LLM key is present, ask the model to produce a summary or rationale
    llm_key = os.getenv("OPENAI_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if llm_key and recommendations:
        print("✅ LLM key found; attempting to generate recommendation rationale.")
        summary_prompt = (
            f"I have the following product matches for a {category}:\n\n"
            + "\n".join(
                [
                    f"{i+1}. {p['name']} (brand: {p['brand']}, color: {p['color']}, price: ₹{p['price']})"
                    for i, p in enumerate(recommendations)
                ]
            )
            + "\n\nBased on the user's preferences (brand="
            + brand
            + ", color="
            + color
            + ", price_range="
            + f"{min_price}-{max_price}"
            + "), which product is most appropriate? Provide a brief rationale."
        )

        try:
            if os.getenv("OPENAI_API_KEY"):
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summary_prompt}],
                    max_tokens=200
                )
                rationale = response.choices[0].message.content.strip()

            else:
                from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
                client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
                claude_input = f"{HUMAN_PROMPT}{summary_prompt}{AI_PROMPT}"
                rationale = client.completions.create(
                    model="claude-3.7-sonnet",
                    prompt=claude_input,
                    max_tokens_to_sample=200
                )["completion"].strip()

            print("\n🤖 LLM Recommendation Rationale:")
            print(rationale)
        except Exception as e:
            print(f"\n⚠️ LLM-based summary failed: {e}")
            print("Proceeding with raw list of products.")

    # 4. Confirmation step
    while True:
        confirm = input("\nIs one of these the correct product? (Y/N): ").strip().lower()
        if confirm == "y":
            if len(recommendations) > 1:
                sel = input(f"Enter the number (1-{len(recommendations)}) of the item you want: ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(recommendations):
                    chosen = recommendations[int(sel) - 1]
                    context["final_product"] = chosen
                    print(f"\n🎉 Final product selected: {chosen['name']} | ₹{chosen['price']} | {chosen['brand']} | {chosen['color']}")
                    return context
                else:
                    print(f"⚠️ Please enter a valid number between 1 and {len(recommendations)}.")
                    continue
            else:
                chosen = recommendations[0]
                context["final_product"] = chosen
                print(f"\n🎉 Final product selected: {chosen['name']} | ₹{chosen['price']} | {chosen['brand']} | {chosen['color']}")
                return context

        elif confirm == "n":
            if not preferences:
                print("⚠️ No preferences to adjust. Restarting clarification.")
                context["preferences"] = {}
                return clarify_preferences(context)

            print("\nWhich attribute would you like to change?")
            available_keys = list(preferences.keys())
            for i, key in enumerate(available_keys, start=1):
                print(f"  {i}. {key}")
            print(f"  {len(available_keys) + 1}. Restart full preferences")

            choice = input(f"Enter a number (1-{len(available_keys) + 1}): ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(available_keys):
                    selected_key = available_keys[choice - 1]
                    new_val = input(f"Enter new value for '{selected_key}': ").strip()
                    while not new_val:
                        print("⚠️ Input cannot be empty.")
                        new_val = input(f"Enter new value for '{selected_key}': ").strip()

                    if selected_key == "price_range":
                        while True:
                            candidate = new_val.replace(" ", "")
                            if "-" in candidate:
                                parts = candidate.split("-")
                                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                    preferences[selected_key] = (int(parts[0]), int(parts[1]))
                                    break
                                else:
                                    print("⚠️ Invalid range. Use 'min-max' format (e.g., 0-20000).")
                            else:
                                if candidate.isdigit():
                                    num = int(candidate)
                                    preferences[selected_key] = (num, num)
                                    break
                                else:
                                    print("⚠️ Enter a numeric value or range (e.g., '1500' or '0-20000').")
                            new_val = input(f"Enter new value for '{selected_key}': ").strip()
                    else:
                        preferences[selected_key] = new_val

                    context["preferences"] = preferences
                    return recommend_product(context)

                elif choice == len(available_keys) + 1:
                    context["preferences"] = {}
                    return clarify_preferences(context)
                else:
                    print(f"⚠️ Invalid selection. Please choose between 1 and {len(available_keys) + 1}.")
                    continue
            else:
                print("⚠️ Please enter a valid number.")
                continue
        else:
            print("⚠️ Please answer 'Y' or 'N'.")
            continue

    return context
