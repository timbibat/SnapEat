"""
Food identification and nutrition retrieval module.
Uses manual input and OpenRouter AI to identify food items.
"""

import base64
import json
import requests
import os
from dotenv import load_dotenv
from backend.food_dataset import get_food_by_name, search_foods, get_all_food_names

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def identify_food_with_openrouter(image_bytes):
    """
    Use OpenRouter's free multimodal models to identify the food item.
    Rotates through multiple free models if one is rate-limited.
    """
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith("your_"):
        print("OpenRouter Error: API key missing or invalid.")
        return None

    # List of free vision models to try in order
    models_to_try = [
        "google/gemini-flash-1.5-8b:free",
        "openrouter/free", 
        "nvidia/llama-3.1-nemotron-70b-instruct:free",
        "qwen/qwen-2-vl-7b-instruct:free"
    ]

    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        for model in models_to_try:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "X-Title": "SnapEat Prototype",
                    },
                    data=json.dumps({
                        "model": model,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Identify the primary food item in this image. Return ONLY the name of the food (e.g., 'Apple', 'Banana', 'Pizza')."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ]
                    }),
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    food_name = result['choices'][0]['message']['content'].strip().lower().replace(".", "")
                    if food_name and food_name != "none":
                        return food_name
                elif response.status_code == 429:
                    print(f"Model {model} is rate-limited, trying next...")
                    continue 
                else:
                    print(f"OpenRouter API Error ({model}): {response.status_code}")
            except Exception as e:
                print(f"OpenRouter Error ({model}): {e}")
                
    except Exception as e:
        print(f"Global OpenRouter Error: {e}")
    
    return None

def identify_food_item(image_data=None, food_name=None):
    """
    Main entry point for food identification.
    Priority: 1. Manual Name (if valid), 2. OpenRouter AI.
    """
    # 1. Manual Name (If user typed something that exists in DB)
    if food_name:
        result = get_food_by_name(food_name)
        if result:
            return {"status": "identified", "food": result, "method": "manual"}

    # 2. AI Identification (If image is provided)
    if image_data:
        ai_guess = identify_food_with_openrouter(image_data)
        if ai_guess:
            result = get_food_by_name(ai_guess)
            if result:
                return {"status": "identified", "food": result, "method": "ai_detection"}

    return None

def get_nutrition_data(food_name):
    food = get_food_by_name(food_name)
    if food:
        return {
            "name": food["name"],
            "category": food["category"],
            "nutrition": food["nutrition"],
            "health_benefits": food["health_benefits"]
        }
    return None

def search_food_items(query):
    results = search_foods(query)
    return [{"name": item["name"], "category": item["category"], "calories": item["nutrition"]["calories"]} for item in results]

def get_available_foods():
    return get_all_food_names()
