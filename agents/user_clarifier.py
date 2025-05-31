import os

def clarify_preferences(context):
    """
    Prompt the user with a set of clarification questions based on the detected product type.
    Uses an LLM (OpenAI GPT-4 or Claude) to generate questions, or falls back to mock questions
    if no API key is provided or if the API call fails.
    """
    # Retrieve the product type from context (default to "product" if not present)
    product_type = context.get("product_type", "product")

    # Present options for which LLM provider to use for question generation
    print("\n🤖 Choose an LLM provider for clarification:")
    print("1. OpenAI GPT-4")
    print("2. Claude 3.7 Sonnet")
    print("3. Mock Mode (No API Key Required)")
    choice = input("Enter 1, 2, or 3: ").strip()  # Read user’s choice

    questions_text = ""  # Will hold the raw markdown question list

    # If the user selects OpenAI GPT-4
    if choice == "1":
        try:
            from openai import OpenAI
            # Initialize OpenAI client using environment variable for API key
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            print("\n🧠 Generating questions using GPT-4...")
            # Build the prompt asking GPT-4 to generate 5 clarifying questions
            prompt = f"""
You're an intelligent shopping assistant. Based on the product type "{product_type}", 
generate 5 clear and helpful questions to understand the user's preferences before recommending a product. 
Include attributes like brand, color, size (if relevant), material (if relevant), price range, or any other specific to the product category.
Return the questions as a markdown bullet list.
"""
            # Send the prompt to GPT-4 and get a response
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            # Extract the generated markdown list of questions
            questions_text = response.choices[0].message.content
        except Exception as e:
            # If there is any error (e.g., missing API key, network issue), print error and switch to mock mode
            print(f"❌ OpenAI error: {e}")
            choice = "3"  # Fallback to mock mode

    # If the user selects Claude 3.7 Sonnet
    if choice == "2":
        try:
            import anthropic
            # Initialize Anthropic client using environment variable for API key
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            # Build a similar prompt for Claude to generate clarifying questions
            prompt = f"""
You're an AI shopping assistant. Given the product type "{product_type}", 
generate 5 thoughtful questions to clarify user preferences (brand, color, size, material, price, etc.).
Return them as a markdown bullet list.
"""
            # Send the prompt to Claude and get a response
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            # Extract the generated markdown list of questions
            questions_text = response.content[0].text
        except Exception as e:
            # If there is any error with Claude, print error and switch to mock mode
            print(f"❌ Claude error: {e}")
            choice = "3"  # Fallback to mock mode

    # If the user chooses mock mode or if no questions were generated
    if choice == "3" or not questions_text:
        print("\n🔧 Running in Mock Mode.")
        # Provide hardcoded question templates based on the product type
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
            # A generic set of fallback questions for any other product category
            questions_text = """
- What brand of product are you interested in?
- What is your preferred color?
- What is your price range?
- Do you have a preferred size?
- Any material or feature preferences?
"""

    # Parse the raw markdown into a list of question strings
    questions = [q.strip("-• ").strip() for q in questions_text.splitlines() if q.strip()]
    # Retrieve (or initialize) existing preferences in the context
    preferences = context.get("preferences", {})

    print("\n🧠 Please answer the following questions:")
    for q in questions:
        # Loop until the user provides a non-empty response for each question
        while True:
            ans = input(f"→ {q}: ").strip()
            if ans:
                break
            print("⚠️ Input cannot be empty. Please provide a valid response.")

        # Heuristically determine a key name based on words in the question
        key_parts = q.lower().split()
        key = None
        for part in ['brand', 'color', 'size', 'material', 'category', 'genre', 'type', 'feature', 'specs', 'price', 'price_range']:
            if part in key_parts:
                key = part
                break
        if not key:
            # If no known keyword found, create a generic preference key
            key = f"preference_{len(preferences) + 1}"
        # Store the user’s answer under the derived key in the preferences dictionary
        preferences[key] = ans

    # If the user provided a "price" answer but not "price_range", copy it over
    if 'price' in preferences and 'price_range' not in preferences:
        preferences['price_range'] = preferences['price']

    # Update the context with the questions asked and the collected preferences
    context["questions"] = questions
    context["preferences"] = preferences
    return context
