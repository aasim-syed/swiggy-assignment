# === File: agents/image_analyzer.py ===
import base64
import os


def analyze_image(context):
    image_b64 = context.get("image_base64")

    if not image_b64:
        context["product_type"] = input("🔍 No image detected. Please manually enter the product category (e.g., sneakers, electronics): ").strip().lower()
        context["error"] = "No image provided, using manual category input."
        return context

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        print("\n🤖 Analyzing image using GPT-4 Vision...")
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this product and infer its category (like sneakers, electronics)."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        description = response.choices[0].message.content
        print(f"\n📷 Vision Output: {description}")
        category = extract_category_from_description(description)
        context["product_type"] = category or "product"
        context["vision_description"] = description
        return context

    except Exception as e:
        print(f"\n⚠️ OpenAI Vision failed: {e}")
        context["product_type"] = input("🔍 Vision failed. Please manually enter the product category (e.g., sneakers, electronics): ").strip().lower()
        context["error"] = "Vision API failed, using manual input"
        return context


def extract_category_from_description(description):
    """
    🔍 Naive keyword matching for category inference.
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
