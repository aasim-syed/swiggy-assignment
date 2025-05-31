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
| 4      | 📚 Books category (branch test)  |                                              [Watch Demo](https://drive.google.com/file/d/1vXcbNMOZJ6-4d0eo3FFnil4EU0UdUbZ7/view?usp=sharing)                                    |
| 5    | install demo  |                                              [Watch Demo](https://drive.google.com/file/d/1V90f2_BKGiHFYOxxLXCbVTmA3dkw4uuY/view?usp=sharing)                                    |

## ⚠️ Note: API-Free Mock Mode Enabled 🧪🚫💳
Since I currently don't have access to an OpenAI or Anthropic API key (credit card required), I’ve painstakingly memorized and replicated their message formats to implement a fully functional Mock Mode 🎭.

This ensures the agent works offline and is API-key ready — just plug in your keys when available 🔑.

🧠 The logic, flow, and architecture mirror production-ready setups, making this ideal for future extension with real API access.


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
## Test instructions:
| Image Purpose            | Raw Image Link                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Sneaker QnA (1)          | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102601.png` |
| Sneaker QnA (2)          | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102609.png` |
| Sneaker QnA (3)          | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102622.png` |
| Final Sneaker Output     | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102724.png` |
| Apple AirPods Output (1) | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102823.png` |
| Apple AirPods Output (2) | `https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102904.png` |

## 🧪 Screenshots

### 🏷️ Sneaker Image Questioning Flow

![Sneaker Step 1](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102601.png)
![Sneaker Step 2](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102609.png)
![Sneaker Step 3](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102622.png)
![Sneaker Final Result](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102724.png)

### 🍏 Apple AirPods Flow

![AirPods Step 1](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102823.png)
![AirPods Step 2](https://raw.githubusercontent.com/aasim-syed/swiggy-assignment/main/test_screenshots/Screenshot%202025-05-31%20102904.png)

### For sneaker
python .\main.py

📸 Image Input Options:
1. Use default image: nike-sneaker
2. Enter local file path
3. Enter an internet image URL
Choose an option (1/2/3): 

choose 1 for quick easier testing 

🤖 Choose an LLM provider for clarification:
1. OpenAI GPT-4
2. Claude 3.7 Sonnet
3. Mock Mode (No API Key Required)
Enter 1, 2, or 3: 1
❌ OpenAI error: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable

🔧 Running in Mock Mode.

🧠 Please answer the following questions:
→ What brand of sneakers are you interested in?:

→ What size do you wear?: 10
→ Do you prefer any material (e.g., mesh, leather)?: mesh

✅ 5 matching products found:
- Nike Air Max White | ₹4500 | Nike | white
- Nike Revolution Red | ₹3100 | Nike | red
- Nike Pegasus Turbo Blue | ₹5500 | Nike | blue
- Nike Court Vision White | ₹4100 | Nike | white
- Nike Air Max White | ₹4500 | Nike | white

🛍️ Final Result:
{
  "image_base64": <base64 was too big>,
  "product_type": "sneakers",
  "error": "Vision API failed, using manual input",
  "questions": [
    "What brand of sneakers are you interested in?",
    "What is your preferred color?",
    "What is your price range?",
    "What size do you wear?",
    "Do you prefer any material (e.g., mesh, leather)?"
  ],
  "preferences": {
    "brand": "nike",
    "preference_2": "red",
    "price": "1000-10000",
    "size": "10",
    "material": "mesh",
    "price_range": "1000-10000"
  },
  "recommendations": [
    {
      "id": 1,
      "name": "Nike Air Max White",
      "brand": "Nike",
      "color": "white",
      "price": 4500
    },
    {
      "id": 5,
      "name": "Nike Revolution Red",
      "brand": "Nike",
      "color": "red",
      "price": 3100
    },
    {
      "id": 12,
      "name": "Nike Pegasus Turbo Blue",
      "brand": "Nike",
      "color": "blue",
      "price": 5500
    },
    {
      "id": 16,
      "name": "Nike Court Vision White",
      "brand": "Nike",
      "color": "white",
      "price": 4100
    },
    {
      "id": 1,
      "name": "Nike Air Max White",
      "brand": "Nike",
      "color": "white",
      "price": 4500,
      "category": "sneakers"
    }
  ]
}


### For electronics

📸 Image Input Options:
1. Use default image: nike-sneaker
2. Enter local file path
3. Enter an internet image URL
Choose an option (1/2/3): 1
🔧 Invoking LangGraph...

⚠️ OpenAI Vision failed: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
🔍 Vision failed. Please manually enter the product category (e.g., sneakers, electronics): electronics

🤖 Choose an LLM provider for clarification:
1. OpenAI GPT-4
2. Claude 3.7 Sonnet
3. Mock Mode (No API Key Required)
Enter 1, 2, or 3: 1
❌ OpenAI error: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable

🔧 Running in Mock Mode.

🧠 Please answer the following questions:
→ Which electronics brand do you prefer?:
🧠 Please answer the following questions:
→ Which electronics brand do you prefer?: apple
→ What category (e.g., phone, laptop, headphones) are you looking for?: headphones
→ What is your budget range?: 10000-30000
→ Any color preference for the device?: white

✅ 1 matching products found:
- Apple AirPods Pro | ₹24999 | Apple | white

🛍️ Final Result:
{
  "image_base64": <base64 was too big>,
  "product_type": "electronics",
  "error": "Vision API failed, using manual input",
  "questions": [
    "Which electronics brand do you prefer?",
    "What category (e.g., phone, laptop, headphones) are you looking for?",
    "What is your budget range?",
    "Any color preference for the device?"
  ],
  "preferences": {
    "brand": "apple",
    "category": "headphones",
    "preference_3": "10000-30000",
    "color": "white"
  },
  "recommendations": [
    {
      "id": 10,
      "name": "Apple AirPods Pro",
      "brand": "Apple",
      "color": "white",
      "price": 24999,
      "category": "electronics, headphones"
    }
  ]
}

### For Books
> python .\main.py
📸 Enter the path to your product image (e.g., sample.jpg): C:\Users\aasim\OneDrive\Pictures\Logo2.png  
🔧 Invoking LangGraph...

⚠️ OpenAI Vision failed: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
🔍 Vision failed. Please manually enter the product category (e.g., sneakers, electronics, books): books

🤖 Choose an LLM provider for clarification:
1. OpenAI GPT-4
2. Claude 3.7 Sonnet
3. Mock Mode (No API Key Required)
Enter 1, 2, or 3: 3

🔧 Running in Mock Mode.

🧠 Please answer the following questions:
→ What genre of books are you interested in?: productivity
→ Do you prefer paperback or hardcover?: hardcover
→ Any specific author or title in mind?: cal
→ What's your budget?: 599
→ Do you prefer new releases or classics?: ne

🛍️ Final Result:
{
  "image_base64": <base64 was too big>,
  "product_type": "books",
  "error": "Vision API failed, using manual input",
  "preferences": {
    "genre": "productivity",
    "preference_2": "hardcover",
    "preference_3": "cal",
    "preference_4": "599",
    "preference_5": "ne"
  },
  "questions": [
    "What genre of books are you interested in?",
    "Do you prefer paperback or hardcover?",
    "Any specific author or title in mind?",
    "What's your budget?",
    "Do you prefer new releases or classics?"
  ],
  "recommendations": [
    {
      "id": 17,
      "name": "Atomic Habits",
      "brand": "Penguin",
      "color": "white",
      "price": 499,
      "category": "books"
    },
    {
      "id": 18,
      "name": "The Alchemist",
      "brand": "HarperCollins",
      "color": "yellow",
      "price": 399,
      "category": "books"
    },
    {
      "id": 19,
      "name": "Ikigai",
      "brand": "Penguin",
      "color": "blue",
      "price": 299,
      "category": "books"
    },
    {
      "id": 20,
      "name": "Deep Work",
      "brand": "Grand Central",
      "color": "black",
      "price": 599,
      "category": "books"
    }
  ]
}
### 🤝 Author
Syed Aasim — AI-First Fullstack Engineer
📧 syedaasim133@gmail.com
🌐 LinkedIn | GitHub

⭐ "Obviously it would be great if I get to work with your team — that’s why I put in all this effort. Even if I don’t, I truly enjoyed building this agentic flow — thinking, unlearning, debugging, and building."