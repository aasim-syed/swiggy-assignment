# === File: agents/image_analyzer.py ===
import base64
import os


def analyze_image(context):
    """
    1. Validate and decode base64 image string.
    2. Call OpenAI Vision to describe the product and infer a category.
    3. If Vision fails or category is not found, fall back to manual input.
    """
    image_b64 = context.get("image_base64")

    # 1. Handle missing image_b64
    if not image_b64:
        context["product_type"] = input(
            "🔍 No image detected. Please manually enter the product category "
            "(e.g., sneakers, electronics): "
        ).strip().lower()
        context["error"] = "No image provided; using manual category input."
        return context

    # 2. Validate and decode base64 data
    try:
        # If image_b64 includes a prefix like "data:image/xxx;base64,", strip it
        if "," in image_b64:
            payload = image_b64.split(",", 1)[1]
        else:
            payload = image_b64
        # Attempt to decode to ensure it is valid base64
        _ = base64.b64decode(payload, validate=True)
    except Exception:
        context["product_type"] = input(
            "⚠️ Uploaded file is not a valid base64 image. "
            "Please enter the product category manually (e.g., sneakers, electronics): "
        ).strip().lower()
        context["error"] = "Invalid base64 image; using manual input."
        return context

    # 3. Call OpenAI Vision API
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        print("\n🤖 Analyzing image using GPT-4 Vision...")
        # Construct a message with text prompt and image URL encoded as data URI
        message_content = [
            {"type": "text", "text": "Describe this product and infer its category (e.g., sneakers, electronics)."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{payload}"
                }
            }
        ]
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{"role": "user", "content": message_content}],
            max_tokens=300
        )

        description = response.choices[0].message.content.strip()
        print(f"\n📷 Vision Output: {description}")

        # Attempt to extract a category from Vision’s description
        category = extract_category_from_description(description)
        if category:
            context["product_type"] = category
            context["vision_description"] = description
            context["error"] = None
        else:
            # If no category keywords found, prompt manual fallback
            print("⚠️ Unable to infer category from Vision output.")
            manual = input(
                "🔍 Please manually enter the product category (e.g., sneakers, electronics): "
            ).strip().lower()
            context["product_type"] = manual or "product"
            context["vision_description"] = description
            context["error"] = "Category not inferred; using manual input."

        return context

    except Exception as e:
        # Vision API call failure
        print(f"\n⚠️ OpenAI Vision failed: {e}")
        context["product_type"] = input(
            "🔍 Vision failed. Please manually enter the product category "
            "(e.g., sneakers, electronics): "
        ).strip().lower()
        context["error"] = "Vision API failed; using manual input."
        return context


def extract_category_from_description(description):
    """
    🔍 Naive keyword matching for category inference.
    Returns a category string if any keyword matches; otherwise None.
    """
    description = description.lower()
    keywords = {
        "sneakers": ["shoe", "sneaker", "trainer"],
        "clothes": ["shirt", "t-shirt", "jeans", "jacket"],
        "electronics": ["laptop", "phone", "camera", "headphones", "airpods", "earbuds"],
        "food": ["burger", "pizza", "cake", "snack"],
        "books": ["book", "novel", "paperback"]
    }

    for category, terms in keywords.items():
        if any(term in description for term in terms):
            return category
    return None
