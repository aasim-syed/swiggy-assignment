import os

def clarify_preferences(context):
    product_type = context.get("product_type", "product")

    print("\n🤖 Choose an LLM provider for clarification:")
    print("1. OpenAI GPT-4")
    print("2. Claude 3.7 Sonnet")
    print("3. Mock Mode (No API Key Required)")
    choice = input("Enter 1, 2, or 3: ").strip()

    questions_text = ""

    if choice == "1":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            print("\n🧠 Generating questions using GPT-4...")
            prompt = f"""
You're an intelligent shopping assistant. Based on the product type "{product_type}", 
generate 5 clear and helpful questions to understand the user's preferences before recommending a product. 
Include attributes like brand, color, size (if relevant), material (if relevant), price range, or any other specific to the product category.
Return the questions as a markdown bullet list.
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            questions_text = response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            choice = "3"

    if choice == "2":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            prompt = f"""
You're an AI shopping assistant. Given the product type "{product_type}", 
generate 5 thoughtful questions to clarify user preferences (brand, color, size, material, price, etc.).
Return them as a markdown bullet list.
"""
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            questions_text = response.content[0].text
        except Exception as e:
            print(f"❌ Claude error: {e}")
            choice = "3"

    if choice == "3" or not questions_text:
        print("\n🔧 Running in Mock Mode.")
        if product_type.lower() == "sneakers":
            questions_text = """
- What brand of sneakers are you interested in?
- What is your preferred color?
- What is your price range?
- What size do you wear?
- Do you prefer any material (e.g., mesh, leather)?
"""
        elif product_type.lower() == "electronics":
            questions_text = """
- Which electronics brand do you prefer?
- What category (e.g., phone, laptop, headphones) are you looking for?
- What is your budget range?
- Any color preference for the device?
"""
        elif product_type.lower() == "books":
            questions_text = """
- What genre of books are you interested in?
- Do you prefer paperback or hardcover?
- Any specific author or title in mind?
- What's your budget?
- Do you prefer new releases or classics?
"""
        else:
            questions_text = """
- What brand of product are you interested in?
- What is your preferred color?
- What is your price range?
- Do you have a preferred size?
- Any material or feature preferences?
"""

    # Parse and ask questions
    questions = [q.strip("-• ").strip() for q in questions_text.splitlines() if q.strip()]
    preferences = context.get("preferences", {})

    print("\n🧠 Please answer the following questions:")
    for q in questions:
        while True:
            ans = input(f"→ {q}: ").strip()
            if ans:
                break
            print("⚠️ Input cannot be empty. Please provide a valid response.")

        # Heuristically assign keys
        key_parts = q.lower().split()
        key = None
        for part in ['brand', 'color', 'size', 'material', 'category', 'genre', 'type', 'feature', 'specs', 'price', 'price_range']:
            if part in key_parts:
                key = part
                break
        if not key:
            key = f"preference_{len(preferences)+1}"
        preferences[key] = ans

    # Normalize price input if needed
    if 'price' in preferences and 'price_range' not in preferences:
        preferences['price_range'] = preferences['price']

    context["questions"] = questions
    context["preferences"] = preferences
    return context
