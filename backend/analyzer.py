"""
Food identification and nutrition retrieval module.
Uses manual input and OpenRouter AI to identify food items.
"""

import base64
import json
import requests
import os
import time
import io
from PIL import Image
from dotenv import load_dotenv
from backend.food_dataset import get_food_by_name, search_foods, get_all_food_names, FOOD_DATABASE

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def identify_food_item(image_data=None, food_name=None):
    """
    Main entry point for food identification.
    Uses the name provided by Puter.js from the frontend.
    """
    if food_name:
        # Try exact match in our database
        result = get_food_by_name(food_name)
        if result:
            return {"status": "identified", "food": result, "method": "puter_ai"}
            
        # Try fuzzy search if not exact match
        search_results = search_foods(food_name)
        if search_results:
            return {"status": "identified", "food": search_results[0], "method": "puter_ai"}
            
        # If the food Puter found isn't in our DB, return a dynamic result
        return {
            "status": "identified", 
            "food": {
                "name": food_name.title(), # Use the actual name found!
                "category": "General",
                "nutrition": {"calories": 100, "carbs": 15, "sugars": 8, "fiber": 3, "protein": 2, "fat": 1},
                "health_benefits": ["Good source of general nutrients", "Supports overall health"],
                "image_url": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=500&q=80"
            },
            "method": "puter_ai"
        }

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
