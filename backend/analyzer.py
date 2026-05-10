"""
Food identification and nutrition retrieval module.
Pure AI Mode: Optimized for maximum reliability and robust JSON parsing.
"""

import os
import google.generativeai as genai
from PIL import Image
import io
import json

# Global model variable
_model = None

def get_model():
    """Dynamically find and initialize a supported multimodal model."""
    global _model
    if _model is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                prefs = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro-vision']
                
                for p in prefs:
                    if p in available_models:
                        # We don't force JSON mode globally here to avoid compatibility issues with older models
                        _model = genai.GenerativeModel(p)
                        print(f"DEBUG: Selected {p} for Pure AI Mode")
                        break
                
                if not _model and available_models:
                    _model = genai.GenerativeModel(available_models[0])
                
            except Exception as e:
                print(f"DEBUG: Gemini Discovery Error: {e}")
    return _model

def clean_and_parse_json(text):
    """Robustly extracts and parses JSON from AI response."""
    text = text.strip()
    try:
        # Try direct parse
        return json.loads(text)
    except:
        # Try to find braces
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != 0:
                return json.loads(text[start:end])
        except:
            print(f"DEBUG: Failed to parse JSON from: {text[:100]}...")
            return None
    return None

def enforce_schema(data, name_fallback="Unknown Food"):
    """Guarantees the food object has all required keys and nested structures for the UI."""
    if not data or not isinstance(data, dict): data = {}
    
    # Define the absolute minimum structure
    schema = {
        "name": data.get("name") or data.get("food_name") or name_fallback,
        "category": data.get("category", "General"),
        "nutrition": {
            "calories": 0, "carbs": 0, "sugars": 0, "fiber": 0,
            "protein": 0, "fat": 0, "vitamin_c": 0, "potassium": 0, "sodium": 0
        },
        "health_benefits": data.get("health_benefits", ["Informative AI analysis"]),
        "age_sensitivity": {
            "kid": {"rating": "Safe", "tips": ["Always check ingredients"]},
            "teen": {"rating": "Safe", "tips": ["Maintain balanced diet"]},
            "adult": {"rating": "Safe", "tips": ["Watch portions"]},
            "elderly": {"rating": "Safe", "tips": ["Easy to digest"]}
        },
        "image_url": data.get("image_url", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=60")
    }
    
    # Deep merge nutrition
    ai_nut = data.get("nutrition", {})
    if isinstance(ai_nut, dict):
        for k in schema["nutrition"]:
            if k in ai_nut:
                try:
                    schema["nutrition"][k] = float(ai_nut[k])
                except: pass
                
    # Deep merge age_sensitivity
    ai_age = data.get("age_sensitivity", {})
    if isinstance(ai_age, dict):
        for age_group in schema["age_sensitivity"]:
            if age_group in ai_age and isinstance(ai_age[age_group], dict):
                # Merge rating and tips
                schema["age_sensitivity"][age_group]["rating"] = ai_age[age_group].get("rating", "Safe")
                if "tips" in ai_age[age_group]:
                    schema["age_sensitivity"][age_group]["tips"] = ai_age[age_group]["tips"]
                    
    return schema

def identify_food_item(image_data=None, food_name=None):
    """Main entry point for AI food analysis."""
    model = get_model()
    if not model: return None

    try:
        if image_data:
            print(f"DEBUG: AI Vision Analysis for image...")
            img = Image.open(io.BytesIO(image_data))
            prompt = """
            Identify this food and provide nutrition facts in JSON format.
            JSON structure: { "name", "category", "nutrition": { "calories", "carbs", "sugars", "fiber", "protein", "fat", "vitamin_c", "potassium", "sodium" }, "health_benefits": [], "age_sensitivity": { "kid": {"rating", "tips":[]}, ... } }
            Include realistic estimates based on portion size.
            """
            response = model.generate_content([prompt, img])
            ai_data = clean_and_parse_json(response.text)
            if ai_data:
                return {"status": "identified", "food": enforce_schema(ai_data), "method": "pure_ai"}

        if food_name:
            print(f"DEBUG: AI Nutrition lookup for: {food_name}")
            prompt = f"Provide nutrition facts for '{food_name}' in this JSON format: {{ 'name', 'category', 'nutrition': {{ 'calories', 'carbs', 'sugars', 'fiber', 'protein', 'fat', 'vitamin_c', 'potassium', 'sodium' }}, 'health_benefits': [], 'age_sensitivity': {{ 'kid': {{'rating', 'tips':[]}}, ... }} }}"
            response = model.generate_content(prompt)
            ai_data = clean_and_parse_json(response.text)
            if ai_data:
                return {"status": "identified", "food": enforce_schema(ai_data, food_name), "method": "pure_ai_text"}

    except Exception as e:
        print(f"DEBUG: AI Analysis Error: {e}")
        
    return None

def get_food_by_name(food_name):
    """UI helper to get food data."""
    if not food_name: return None
    clean_name = food_name.replace("_", " ").title()
    res = identify_food_item(food_name=clean_name)
    return res["food"] if res else enforce_schema({}, clean_name)

def get_nutrition_data(food_name):
    return get_food_by_name(food_name)

def search_food_items(query):
    return []

def get_available_foods():
    return []
