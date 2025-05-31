# === File: agents/image_analyzer.py ===

import os       # For accessing environment variables (e.g., OPENAI_API_KEY)

def analyze_image(context):
    """
    TODO:
    Analyze the provided image (Base64 string) using GPT-4 Vision to infer product category.
    If no image is found or if the Vision API call fails, prompt the user for manual input.
    """
    # Retrieve the Base64-encoded image from context
    image_b64 = context.get("image_base64")

    # If no image is present in the context, fall back to manual category input
    if not image_b64:
        # Prompt the user to type in a product category, store it in context
        context["product_type"] = input(
            "🔍 No image detected. Please manually enter the product category (e.g., sneakers, electronics): "
        ).strip().lower()
        # Record an error message indicating that Vision was bypassed
        context["error"] = "No image provided, using manual category input."
        return context

    try:
        # Dynamically import the OpenAI client only if an image is present
        from openai import OpenAI
        # Initialize the OpenAI client using the API key from environment variables
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        print("\n🤖 Analyzing image using GPT-4 Vision...")
        # Send a chat completion request to GPT-4 Vision with both text prompt and image
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        # First element: text prompt instructing the model to describe the product
                        {"type": "text", "text": "Describe this product and infer its category (like sneakers, electronics)."},
                        # Second element: the actual image data as a Base64-encoded data URL
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300  # Limit the response to 300 tokens for efficiency
        )

        # Extract the model's textual description from the response
        description = response.choices[0].message.content
        print(f"\n📷 Vision Output: {description}")

        # Attempt to infer a category based on keywords in the description
        category = extract_category_from_description(description)
        # Store the inferred category in context; default to generic "product" if inference failed
        context["product_type"] = category or "product"
        # Save the full vision description for possible downstream use or debugging
        context["vision_description"] = description
        return context

    except Exception as e:
        # If any error occurs (e.g., missing API key, network failure), print a warning
        print(f"\n⚠️ OpenAI Vision failed: {e}")
        # Prompt the user to manually enter a product category
        context["product_type"] = input(
            "🔍 Vision failed. Please manually enter the product category (e.g., sneakers, electronics): "
        ).strip().lower()
        # Record an error message indicating Vision API failure
        context["error"] = "Vision API failed, using manual input"
        return context


def extract_category_from_description(description):
    """
    🔍 Naive keyword matching for category inference.
    Scans the description text for known product-related keywords.
    Returns the first matching category or None if no keywords are found.
    """
    # Normalize the description to lowercase for case-insensitive matching
    description = description.lower()

    # Map potential categories to lists of indicative keywords
    keywords = {
        "sneakers": ["shoe", "sneaker", "trainer"],
        "clothes": ["shirt", "t-shirt", "jeans", "jacket"],
        "electronics": ["laptop", "phone", "camera", "headphones", "airpods", "earbuds"],
        "food": ["burger", "pizza", "cake", "snack"],
        "books": ["book", "novel", "paperback"]
    }

    # Iterate through each category and its associated terms
    for category, terms in keywords.items():
        # If any of the terms appear in the description, return this category
        if any(term in description for term in terms):
            return category

    # If no matching keywords are found, return None
    return None
