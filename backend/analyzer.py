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

NON_FOOD_TERMS = {
    "food", "tableware", "plate", "dish", "cuisine", "ingredient", "produce", 
    "fruit", "vegetable", "sweet", "baked goods", "comfort food", "recipe", 
    "natural foods", "whole food", "vegan nutrition", "staple food", "yellow",
    "red", "green", "orange", "cooking", "meal", "brunch", "breakfast", "dinner",
    "lunch", "finger food", "fast food", "fastfood", "snack", "snacks", "bowl", "bowls",
    "cup", "cups", "container", "containers", "sauce", "sauces", "utensil", "utensils",
    "logo", "logos", "brand", "branding", "trademark", "product", "goods", "packaging",
    "package", "label", "labels", "advertising", "advertisement", "sign", "sticker", "stickers",
    "text", "font", "writing", "lettering", "alphabet", "word", "color", "blue", "brown", 
    "black", "white", "purple", "pink", "graphic", "graphics", "graphic design", "design", 
    "art", "illustration", "clipart", "drawing", "plastic", "paper", "bag", "box", "carton", "wrapper"
}

def convert_to_jpeg(image_bytes):
    """
    Standardizes any uploaded image format (PNG, WEBP, etc.) into a compressed JPEG 
    using Pillow, and returns the standardized JPEG bytes.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA/P formats to RGB so it can be saved as JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Downscale if image is excessively large to save bandwidth & latency
        max_size = 1024
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=85)
        return output.getvalue()
    except Exception as e:
        print(f"Error standardizing image format: {e}")
        return image_bytes

def query_google_vision(image_data):
    """
    Sends base64 encoded image to Google Cloud Vision API and returns identified labels.
    """
    if image_data:
        print(f"DEBUG: original image_data size is {len(image_data)} bytes")
        image_data = convert_to_jpeg(image_data)
        print(f"DEBUG: standardized JPEG size is {len(image_data)} bytes")
        
    api_key = os.getenv("GOOGLE_VISION_API_KEY")
    if not api_key or "your_google_vision_api_key" in api_key:
        print("Warning: GOOGLE_VISION_API_KEY is not configured or is placeholder in .env.")
        return []

    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    
    # Base64 encode the binary image data
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        "requests": [
            {
                "image": {
                    "content": base64_image
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 15
                    },
                    {
                        "type": "OBJECT_LOCALIZATION",
                        "maxResults": 15
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        labels = []
        responses = data.get("responses", [])
        if not responses:
            return []
            
        res = responses[0]
        if "error" in res:
            print(f"Google Vision API Response Error: {res['error']}")
            return []
        
        # 1. Parse Object Localization (typically specific objects e.g. "Apple", "Banana")
        for obj in res.get("localizedObjectAnnotations", []):
            name = obj.get("name")
            if name:
                labels.append(name.strip().lower())
                
        # 2. Parse Label Detection
        for label in res.get("labelAnnotations", []):
            desc = label.get("description")
            if desc:
                labels.append(desc.strip().lower())
                
        # Remove duplicates while maintaining order
        unique_labels = []
        for l in labels:
            if l not in unique_labels:
                unique_labels.append(l)
                
        return unique_labels
        
    except Exception as e:
        print(f"Google Vision API Request Error: {e}")
        return []

def match_labels_to_food(labels):
    """
    Given a list of labels from Google Vision, find the best matching food in datasets.
    """
    from backend.food_dataset import FOOD_DATABASE, load_kaggle_food
    
    cleaned_labels = [l.lower().strip() for l in labels if l]
    
    # Step 1: Search for an EXACT or plural match in the high-quality static database for ALL labels first
    for label in cleaned_labels:
        query_id = label.replace(" ", "_")
        if query_id in FOOD_DATABASE:
            print(f"DEBUG: Matched exact static food for label '{label}': {FOOD_DATABASE[query_id]['name']}")
            return FOOD_DATABASE[query_id]
            
    # Step 2: Search for "contains" or singular/plural relations in the static database for ALL labels
    for label in cleaned_labels:
        if label in NON_FOOD_TERMS:
            continue  # Skip generic terms
            
        for key, data in FOOD_DATABASE.items():
            key_name = data["name"].lower()
            is_plural_match = (label + "s" == key) or (label + "es" == key) or (key + "s" == label) or (key + "es" == label)
            if f" {label} " in f" {key_name} " or is_plural_match:
                print(f"DEBUG: Matched partial static food for label '{label}': {data['name']}")
                return data
                
    # Step 3: Search the Kaggle database for matches for non-generic labels
    for label in cleaned_labels:
        if label in NON_FOOD_TERMS:
            continue
            
        kaggle_result = load_kaggle_food(label)
        if kaggle_result:
            print(f"DEBUG: Matched Kaggle food for label '{label}': {kaggle_result['name']}")
            return kaggle_result
            
    # Step 4: If no database match, return the first label that is not a generic food term
    for label in cleaned_labels:
        if label not in NON_FOOD_TERMS:
            print(f"DEBUG: Dynamic fallback for label '{label}'")
            return get_food_by_name(label)
            
    # Step 5: Ultimate fallback
    fallback_label = cleaned_labels[0] if cleaned_labels else "apple"
    print(f"DEBUG: Ultimate fallback to '{fallback_label}'")
    return get_food_by_name(fallback_label)

def identify_food_item(image_data=None, food_name=None):
    """
    Main entry point for food identification.
    Uses Google Cloud Vision API if binary image_data is provided,
    otherwise matches manual food_name lookup.
    """
    # 1. Manual search/override
    if food_name:
        result = get_food_by_name(food_name)
        if result:
            return {"status": "identified", "food": result, "method": "manual_search"}
            
    # 2. Image scan recognition
    if image_data:
        labels = query_google_vision(image_data)
        print(f"Google Cloud Vision detected labels: {labels}")
        
        if labels:
            matched_food = match_labels_to_food(labels)
            if matched_food:
                return {"status": "identified", "food": matched_food, "method": "google_vision"}
                
        # Graceful fallback (e.g. if API key is missing or fails, default to Apple)
        print("Bypassing Google Cloud Vision API (Key missing/error). Using graceful fallback.")
        fallback_food = get_food_by_name("apple")
        return {"status": "identified", "food": fallback_food, "method": "graceful_fallback"}

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
