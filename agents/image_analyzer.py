from PIL import Image
import io, base64

def analyze_image(context):
    img_data = context.get("image_base64")
    try:
        image = Image.open(io.BytesIO(base64.b64decode(img_data)))
        # mock output: product category = "sneakers"
        context["product_type"] = "sneakers"
        return context
    except Exception as e:
        context["error"] = "Invalid image format"
        return context
