import os

def clarify_preferences(context):
    product_type = context.get("product_type", "product")
    preferences = context.get("preferences", {})
    questions_text = ""

    # Default to mock if nothing is configured
    provider = "mock"

    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
            provider = "openai"
        except Exception as e:
            context["llm_error"] = f"OpenAI error: {e}"

    elif os.getenv("ANTHROPIC_API_KEY"):
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
            provider = "claude"
        except Exception as e:
            context["llm_error"] = f"Claude error: {e}"

    if not questions_text or provider == "mock":
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
        context["mock_mode"] = True

    questions = [q.strip("-• ").strip() for q in questions_text.splitlines() if q.strip()]
    context["questions"] = questions
    context["preferences"] = preferences  # Empty at this point; filled by frontend

    return context
