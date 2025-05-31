import os

def clarify_preferences(context):
    product_type = context.get("product_type", "product")

    # Prompt user to select LLM provider
    print("\n🤖 Choose an LLM provider for clarification:")
    print("1. OpenAI GPT-4")
    print("2. Claude 3.7 Sonnet")
    print("3. Mock Mode (No API Key Required)")
    choice = input("Enter 1, 2, or 3: ").strip()

    questions_text = ""
    if choice == "1":
        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            prompt = f"""
Given the product type "{product_type}", generate 3 clarifying questions 
to understand the user's preferences better (e.g., brand, color, size, price).
Return as a bullet list.
"""
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            questions_text = response['choices'][0]['message']['content']
        except Exception as e:
            print(f"OpenAI error: {str(e)}")
            choice = "3"  # Fallback to mock mode

    if choice == "2":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            prompt = f"""
Given the product type "{product_type}", generate 3 clarifying questions 
to understand the user's preferences better (e.g., brand, color, size, price).
Return as a bullet list.
"""
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            questions_text = response.content[0].text
        except Exception as e:
            print(f"Claude error: {str(e)}")
            choice = "3"  # Fallback to mock mode

    if choice == "3":
        # Mock responses for testing without API keys
        print("\n🔧 Running in Mock Mode.")
        questions_text = """
- What brand of product are you interested in?
- What is your preferred color?
- What is your price range?
"""

    # Process and ask questions
    questions = [q.strip("-• ").strip() for q in questions_text.splitlines() if q.strip()]
    print("\n🧠 Please answer the following:")
    preferences = context.get("preferences", {})
    for q in questions:
        while True:
            ans = input(f"→ {q}: ").strip()
            if ans:
                break
            print("Input cannot be empty. Please provide a valid response.")
        # Extract the key from the question
        key_parts = q.lower().split()
        key = None
        for part in ['brand', 'color', 'size', 'price', 'price_range']:
            if part in key_parts:
                key = part
                break
        if not key:
            key = 'preference'
        preferences[key] = ans

    # Ensure 'brand' key exists in preferences
    if 'brand' not in preferences or preferences['brand'] is None:
        preferences['brand'] = 'Any'  # Set a default value

    context["questions"] = questions
    context["preferences"] = preferences
    return context
