def analyze_image(context):
    image_b64 = context.get("image_base64")

    # Simulate image analysis (mock/fallback mode)
    if not image_b64:
        context["product_type"] = "product"
        context["error"] = "No image provided"
        return context

    try:
        from openai import OpenAI
        client = OpenAI(api_key="sk-...")
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this product and infer its category."},
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
        description = response['choices'][0]['message']['content']
        context["product_type"] = extract_category_from_description(description) or "product"
        return context

    except Exception as e:
        print(f"⚠️ OpenAI Vision failed: {e}")
        # Fallback to mock category
        context["product_type"] = "sneakers"  # Or use "product"
        context["error"] = "Vision failed; using mock category"
        return context


def extract_category_from_description(description):
    """
    Naive keyword-based extraction from the description.
    """
    keywords = ["shoes", "sneakers", "t-shirt", "laptop", "headphones", "watch"]
    description = description.lower()
    for word in keywords:
        if word in description:
            return word
    return None
