import base64
import json
import os
import requests
from graph import build_graph

def get_image_base64():
    print("\n📸 Image Input Options:")
    print("1. Use default image: nike-sneaker")
    print("2. Enter local file path")
    print("3. Enter an internet image URL")
    
    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        file_path = os.path.join(os.path.dirname(__file__), "nike-sneaker.jpg")
        if not os.path.exists(file_path):
            print("❌ Default image not found.")
            return None
        try:
            with open(file_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            print(f"❌ Failed to read default image: {e}")
            return None

    elif choice == "2":
        file_path = input("📁 Enter the path to your product image: ").strip()
        try:
            with open(file_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            print(f"❌ Failed to read image: {e}")
            return None

    elif choice == "3":
        url = input("🌐 Enter the image URL: ").strip()
        try:
            response = requests.get(url)
            response.raise_for_status()
            return base64.b64encode(response.content).decode("utf-8")
        except Exception as e:
            print(f"❌ Failed to download image: {e}")
            return None

    else:
        print("⚠️ Invalid option.")
        return None

# Invoke LangGraph pipeline
image_b64 = get_image_base64()

if image_b64:
    print("🔧 Invoking LangGraph...")
    try:
        graph = build_graph()
        result = graph.invoke({"image_base64": "image_b64_value_comes_here"})
        print("\n🛍️ Final Result:\n" + json.dumps(result, indent=2))
    except Exception as e:
        print("❌ Error while invoking graph:", e)
else:
    print("🚫 No image provided. Exiting.")
