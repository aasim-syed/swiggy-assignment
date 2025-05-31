# swiggy-assignment# 🛍️ AI Shopping Assistant (LangGraph + GPT-4 Vision + Claude)

A multi-turn conversational AI agent that understands your product preferences from images 🖼️ or user chat 🧠 and recommends items from a local catalog — all powered by **LangGraph**, **GPT-4 Vision**, and **Claude 3.7 Sonnet**.

> Built with ❤️ for smart, adaptive, and delightful shopping experiences.

---

## ✨ Features

### 📸 Image-Driven Intelligence
- Upload any **product image** (e.g., a sneaker or gadget).
- GPT-4 Vision analyzes the image and **infers the product type** automatically.
- No need for manual tagging or labeling!

### 💬 Adaptive Clarification (LLM-Powered)
- The agent **asks tailored follow-up questions** depending on product category.
  - E.g., "What size?" for sneakers or "What features?" for electronics.
- Choose from:
  - **GPT-4** (via OpenAI)
  - **Claude 3.5 Sonnet** (via Anthropic)
  - **Mock mode** (for offline/local testing)

### 🧠 Smart Recommendation Engine
- Matches against a curated `mock_products.json` database.
- Flexible filters:
  - 🎯 Brand
  - 🎨 Color
  - 💸 Price range
  - 📦 Category
  - 🧩 Feature preferences
- Works even when preferences are vague or missing — thanks to fuzzy matching.

### 📂 Robust CLI Interaction
- Choose to:
  - Upload your own image,
  - Use a **default image (`nike-sneaker.jpg`)**, or
  - Paste an **image URL** (auto-downloads and converts to base64).

📹 Demo Videos
Explore how the agent works across different scenarios:

| ✅ Test | Description                      | 🎥 Video Link                                                                                    |
| ------ | -------------------------------- | ------------------------------------------------------------------------------------------------ |
| 1      | 🎯 Sneakers with specific color  | [Watch Demo](https://drive.google.com/file/d/1DN2-LhjZ6gx2PYUF-AJVdNv44hVvggJn/view?usp=sharing) |
| 2      | 🎨 Sneakers with any color/brand | [Watch Demo](https://drive.google.com/file/d/1sDF7lJ9F4CRryMclxZPhsyGfl_ymk1U_/view?usp=sharing) |
| 3      | 🔌 Electronics flow (Apple)      | [Watch Demo](https://drive.google.com/file/d/1oJpXO5Sl2VBanqqPFv3FN081kUo2She1/view?usp=sharing) |
| 4      | 📚 Books category (branch test)  |                                              [Watch Demo](https://drive.google.com/file/d/1oJpXO5Sl2VBanqqPFv3FN081kUo2She1/view?usp=sharing)                                    |
| 5    | install demo  |                                              [Watch Demo](https://drive.google.com/file/d/1V90f2_BKGiHFYOxxLXCbVTmA3dkw4uuY/view?usp=sharing)                                    |

### ⚙️ Extensible Graph Architecture (via LangGraph)
- Modular agent nodes:
  - `image_analyzer`
  - `user_clarifier`
  - `product_recommender`
- Easy to extend with new nodes (e.g., vector search, real-time price lookup).

---

## 🧪 File Tree (Backend)



---

## ⚙️ Setup & Run

### 🔧 Install Requirements
```bash
pip install -r requirements.txt
```

### 🚀 Start the App
```bash
python main.py
```
```bash
Follow the interactive CLI:

Upload image

Answer questions

Get recommendations!
```

## 📦 Product Categories Supported
Category	Attributes Asked
Sneakers	Brand, Color, Size, Material, Price
Electronics	Brand, Subcategory, Color, Specs, Budget
Clothes	Brand, Color, Size, Type, Budget
Books	Genre, Author, Format, Budget, Language
Food	Cuisine, Type, Brand, Flavor, Price

More can be added in seconds 🔧

### 🛠️ Tech Stack
Layer	Stack
Backend	Python + LangGraph + OpenAI/Claude
LLMs	GPT-4 Vision, Claude 3.5 Sonnet
Image	Base64 processing + PIL + requests
Data Store	Local JSON catalog
Dev Tools	Vite (for upcoming React frontend)

### 🌱 Upcoming (Optional React UI)
Want a beautiful frontend? Just run:


```bash
npm create vite@latest shopping-assistant-ui
(coming soon in /frontend)
```

### 🙌 Why This Matters
🧠 Demonstrates multi-agent reasoning (Vision + LLM + logic)

🪄 Blends computer vision and language understanding

📦 Real-world application: AI product assistants

⚙️ Easily extensible to web apps or e-commerce APIs

### 💡 Ideal For:
Job portfolios 🧳

Smart assistants 🧠

Hackathons ⚔️

Open source contributions 🤝

### 🤝 Author
Syed Aasim — AI-First Fullstack Engineer
📧 syedaasim133@gmail.com
🌐 LinkedIn | GitHub

⭐ "Obviously it would be great if I get to work with your team — that’s why I put in all this effort. Even if I don’t, I truly enjoyed building this agentic flow — thinking, unlearning, debugging, and building."