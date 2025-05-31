import base64
import os


def analyze_image(context):
    image_b64 = context.get("image_base64")

    if not image_b64:
        context["product_type"] = None
        context["error"] = "No image provided."
        return context

    # Try real Vision API if OPENAI_API_KEY is set
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)

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
            context["error"] = f"Vision API failed: {str(e)}"

    # 🔧 Fallback: Mock mode if API fails or not set
    print("🔁 Running in Mock Mode (Vision fallback).")
    context["product_type"] = None  # default fallback category
    context["vision_description"] = "Mock mode: default category set to electronics"
    context["mock_mode"] = True
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
