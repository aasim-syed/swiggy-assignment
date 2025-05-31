import base64
import json
from graph import build_graph

def get_image_base64():
    file_path = input("📸 Enter the path to your product image (e.g., sample.jpg): ")
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ Failed to read image: {e}")
        return None

image_b64 = get_image_base64()

if image_b64:
    print("🔧 Invoking LangGraph...")
    try:
        graph = build_graph()
        result = graph.invoke({"image_base64": image_b64})
        print("\n🛍️ Final Result:\n" + json.dumps(result, indent=2))
    except Exception as e:
        print("❌ Error while invoking graph:", e)
else:
    print("🚫 No image provided. Exiting.")
