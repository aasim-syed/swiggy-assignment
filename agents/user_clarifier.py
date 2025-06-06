# === File: agents/user_clarifier.py ===

import os
from difflib import get_close_matches

# (keep the same mock schema as before)
mock_questions_schema = {
    "sneakers": [
        ("What brand of sneakers are you interested in?", "brand"),
        ("What is your preferred color?", "color"),
        ("What is your price range? (e.g., 0-5000)", "price_range"),
        ("What size do you wear?", "size"),
        ("Do you prefer any material (e.g., mesh, leather)?", "material"),
    ],
    "electronics": [
        ("Which electronics brand do you prefer?", "brand"),
        ("What category (e.g., phone, laptop, headphones) are you looking for?", "category"),
        ("What is your budget range? (e.g., 0-20000)", "price_range"),
        ("Any color preference for the device?", "color"),
    ],
    "books": [
        ("What genre of books are you interested in?", "genre"),
        ("Do you prefer paperback or hardcover?", "format"),
        ("Any specific author or title in mind?", "author_or_title"),
        ("What's your budget? (e.g., 0-500)", "price_range"),
        ("Do you prefer new releases or classics?", "preference"),
    ],
    "default": [
        ("What brand of product are you interested in?", "brand"),
        ("What is your preferred color?", "color"),
        ("What is your price range? (e.g., 0-10000)", "price_range"),
        ("Do you have a preferred size?", "size"),
        ("Any material or feature preferences?", "features"),
    ],
}

def clarify_preferences(context):
    """
    1. Determine which question schema to use by fuzzy-matching product_type.
    2. If OPENAI_API_KEY or CLAUDE_API_KEY is set, invoke the LLM to generate questions.
    3. Otherwise, fall back to the mock_questions_schema.
    4. For each needed question, validate and loop until the user provides a non-empty answer.
    """
    print("Context at start of clarification:")
    print(context)

    product_type = context.get("product_type", "product").strip().lower()
    preferences = context.get("preferences", {})

    # 1. Pick schema key by fuzzy-matching
    schema_key = product_type if product_type in mock_questions_schema else None
    if schema_key is None:
        close = get_close_matches(product_type, mock_questions_schema.keys(), n=1, cutoff=0.6)
        if close:
            schema_key = close[0]
            print(f"🤖 Using fuzzy-matched product type: '{schema_key}'\n")
        else:
            print("🤖 No close match found. Falling back to 'default'.\n")
            schema_key = "default"

    # 2. If an LLM key is present, ask the model to generate 5 questions
    questions = []
    llm_key = os.getenv("OPENAI_API_KEY") or os.getenv("CLAUDE_API_KEY")
    # In agents/user_clarifier.py, inside clarify_preferences:

    llm_key = os.getenv("OPENAI_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if not llm_key:
        print("⚠️ No OpenAI or Claude key found; using mock questions.")
    else:
        print("✅ Found LLM key; will attempt to generate questions via LLM.")

    if llm_key:
        # Build a prompt that requests brand/color/size/price-based questions
        prompt = (
            f"You are an AI shopping assistant. The user wants a {schema_key}. "
            "Generate 5 clear questions to clarify their preferences, focusing on brand, color, "
            "size (if relevant), material (if relevant), and price range."
        )

        try:
            if os.getenv("OPENAI_API_KEY"):
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                llm_output = response.choices[0].message.content.strip()

            else:
                # Example pseudocode for Claude 3.7 Sonnet; replace with your actual Claude client
                from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
                client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
                # Wrap prompt for Claude’s format
                claude_prompt = f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}"
                llm_output = client.completions.create(
                    model="claude-3.7-sonnet",
                    prompt=claude_prompt,
                    max_tokens_to_sample=200
                )["completion"].strip()

            # Split into lines and trim to get the question text
            for line in llm_output.split("\n"):
                stripped = line.strip()
                if stripped:
                    questions.append((stripped, None))  # We set key=None for now; you can heuristically assign a key later
            print("\n🤖 LLM-generated questions:")
            for q, _ in questions:
                print("  •", q)

        except Exception as e:
            print(f"⚠️ LLM call failed: {e}")
            llm_key = None  # Fallback to mock mode

    # 3. Fallback to mock mode if no LLM key or LLM call failed
    if not questions:
        schema = mock_questions_schema[schema_key]
        questions = schema  # each item is (question_text, key)

    print("\n🧠 Clarification Phase")
    print(f"Using schema: '{schema_key}'\n")

    # 4. Ask each question in order, skipping ones already answered
    for question_text, key in questions:
        # If we generated keys via LLM, they may be None; fall back to a simple guess:
        if key is None:
            # e.g., “What brand of X?” → key = "brand"; “Any color preference?” → key = "color"
            lowered = question_text.lower()
            if "brand" in lowered:
                key = "brand"
            elif "color" in lowered:
                key = "color"
            elif "price" in lowered:
                key = "price_range"
            elif "size" in lowered:
                key = "size"
            elif "author" in lowered or "genre" in lowered:
                key = "author_or_title" if "author" in lowered else "genre"
            else:
                key = "other"

        existing = preferences.get(key, "")
        if isinstance(existing, str) and existing.strip():
            continue

        while True:
            ans = input(f"→ {question_text} ").strip()
            if not ans:
                print("⚠️ Input cannot be empty. Please provide a valid response.")
                continue

            # Special validation for price_range
            if key == "price_range":
                candidate = ans.replace(" ", "")
                if "-" in candidate:
                    parts = candidate.split("-")
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        low, high = int(parts[0]), int(parts[1])
                        if low > high:
                            print("⚠️ Minimum cannot exceed maximum. Use 'min-max'.")
                            continue
                        preferences[key] = (low, high)
                        break
                    else:
                        print("⚠️ Invalid range format. Please enter as 'min-max'.")
                        continue
                elif candidate.isdigit():
                    num = int(candidate)
                    preferences[key] = (0, num)
                    break
                else:
                    print("⚠️ Invalid number. Enter numeric or range.")
                    continue

            # For all other keys, store as plain string
            preferences[key] = ans
            break

    context["preferences"] = preferences
    return context
