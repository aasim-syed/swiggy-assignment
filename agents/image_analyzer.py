from openai import OpenAI

client = OpenAI(api_key="sk-...")

def analyze_image(context):
    image_b64 = context.get("image_base64")
    try:
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
        output = response['choices'][0]['message']['content']
        print("🔍 GPT Vision Response:", output)
        context["product_type"] = output.strip()
        return context
    except Exception as e:
        context["error"] = f"Vision failed: {str(e)}"
        return context
