"""
Food Nutrition Dataset for SnapEat/FoodAi.
Contains nutritional data, health benefits, and age-specific recommendations
for common food items.
"""

FOOD_DATABASE = {
    # === FRUITS ===
    "apple": {
        "name": "Apple",
        "category": "Fruit",
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6faa6?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 95, "carbs": 25, "sugars": 19,
            "fiber": 4, "protein": 0.5, "fat": 0.3,
            "vitamin_c": 14, "potassium": 195, "sodium": 2
        },
        "health_benefits": [
            "Good for digestion (high fiber)",
            "Supports immune system (Vitamin C)",
            "Helps heart health",
            "Low in calories, good for weight management"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Supports Growth and Immunity", "Good for teeth", "Brain Support"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Weight Management", "Skin Health", "Focus & Memory"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Blood Sugar Control", "Weight Control", "Gut Health"]},
            "elderly": {"rating": "Highly Recommended", "tips": ["Supports Digestion", "Heart protection", "Bone Support"]}
        }
    },
    "banana": {
        "name": "Banana",
        "category": "Fruit",
        "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 105, "carbs": 27, "sugars": 14,
            "fiber": 3.1, "protein": 1.3, "fat": 0.4,
            "vitamin_c": 10, "potassium": 422, "sodium": 1
        },
        "health_benefits": [
            "Excellent source of potassium",
            "Provides quick natural energy",
            "Supports heart and muscle function",
            "Good source of Vitamin B6"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Energy for active play", "Easy to digest", "Supports growth"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Pre-workout fuel", "Muscle support", "Mood booster"]},
            "adult":   {"rating": "Recommended", "tips": ["Heart health", "Blood pressure control", "Quick energy"]},
            "elderly": {"rating": "Highly Recommended", "tips": ["Potassium for heart", "Easy to chew", "Prevents cramps"]}
        }
    },
    "orange": {
        "name": "Orange",
        "category": "Fruit",
        "image_url": "https://images.unsplash.com/photo-1547514701-42782101795e?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 62, "carbs": 15.4, "sugars": 12,
            "fiber": 3.1, "protein": 1.2, "fat": 0.2,
            "vitamin_c": 70, "potassium": 237, "sodium": 0
        },
        "health_benefits": [
            "Very high in Vitamin C",
            "Boosts immune system",
            "Rich in antioxidants",
            "Supports skin health"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Immune system boost", "Hydration", "Healthy snack"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Skin clarity", "Immune defense", "Vitamin C source"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Antioxidant protection", "Heart health", "Iron absorption"]},
            "elderly": {"rating": "Recommended", "tips": ["Immune support", "Anti-inflammatory", "May cause acidity"]}
        }
    },
    "grapes": {
        "name": "Grapes",
        "category": "Fruit",
        "image_url": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 69, "carbs": 18, "sugars": 15,
            "fiber": 0.9, "protein": 0.7, "fat": 0.2,
            "vitamin_c": 11, "potassium": 191, "sodium": 2
        },
        "health_benefits": [
            "Rich in antioxidants (resveratrol)",
            "Supports heart health",
            "Good for eye health",
            "Natural source of hydration"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Recommended", "tips": ["Cut in half to avoid choking", "Natural sweetness", "Hydrating"]},
            "teen":    {"rating": "Recommended", "tips": ["Healthy snack alternative", "Skin health", "Antioxidants"]},
            "adult":   {"rating": "Recommended", "tips": ["Heart health", "Anti-aging properties", "Moderate sugar"]},
            "elderly": {"rating": "Recommended", "tips": ["Easy to eat", "Heart protective", "Watch sugar intake"]}
        }
    },
    "mango": {
        "name": "Mango",
        "category": "Fruit",
        "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 99, "carbs": 25, "sugars": 23,
            "fiber": 2.6, "protein": 1.4, "fat": 0.6,
            "vitamin_c": 60, "potassium": 277, "sodium": 2
        },
        "health_benefits": [
            "Very high in Vitamin A and C",
            "Boosts immunity",
            "Aids digestion with enzymes",
            "Promotes eye health"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Vitamin A for eyesight", "Immune boost", "Tasty and nutritious"]},
            "teen":    {"rating": "Recommended", "tips": ["Skin health", "Energy source", "High in sugar – moderate intake"]},
            "adult":   {"rating": "Recommended", "tips": ["Eye health", "Digestive aid", "Watch portion size"]},
            "elderly": {"rating": "Moderate", "tips": ["High sugar content", "Good vitamins", "Eat in moderation"]}
        }
    },

    # === VEGETABLES ===
    "broccoli": {
        "name": "Broccoli",
        "category": "Vegetable",
        "image_url": "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 55, "carbs": 11, "sugars": 2.6,
            "fiber": 5.1, "protein": 3.7, "fat": 0.6,
            "vitamin_c": 135, "potassium": 457, "sodium": 33
        },
        "health_benefits": [
            "Extremely high in Vitamin C and K",
            "Cancer-fighting properties",
            "High fiber supports gut health",
            "Anti-inflammatory compounds"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Bone building (Vitamin K)", "Immune support", "Brain development"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Skin health", "Strong bones", "Study performance"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Cancer prevention", "Heart health", "Weight management"]},
            "elderly": {"rating": "Highly Recommended", "tips": ["Bone density", "Anti-inflammatory", "Digestive health"]}
        }
    },
    "carrot": {
        "name": "Carrot",
        "category": "Vegetable",
        "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 41, "carbs": 10, "sugars": 4.7,
            "fiber": 2.8, "protein": 0.9, "fat": 0.2,
            "vitamin_c": 6, "potassium": 320, "sodium": 69
        },
        "health_benefits": [
            "Excellent source of beta-carotene (Vitamin A)",
            "Promotes eye health and vision",
            "Good for skin and hair",
            "Supports immune function"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Eye health development", "Crunchy healthy snack", "Immune support"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Skin clarity", "Eye protection", "Low calorie snack"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Eye health maintenance", "Skin anti-aging", "Heart health"]},
            "elderly": {"rating": "Highly Recommended", "tips": ["Vision support", "Easy to cook soft", "Gentle on stomach"]}
        }
    },

    # === PROTEINS ===
    "chicken_breast": {
        "name": "Chicken Breast",
        "category": "Protein",
        "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 165, "carbs": 0, "sugars": 0,
            "fiber": 0, "protein": 31, "fat": 3.6,
            "vitamin_c": 0, "potassium": 256, "sodium": 74
        },
        "health_benefits": [
            "Excellent lean protein source",
            "Supports muscle growth and repair",
            "Low in fat and carbs",
            "Rich in B vitamins"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Growth and muscle development", "Brain function", "Easy to prepare"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Muscle building", "Athletic performance", "High protein for growth"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Lean protein source", "Muscle maintenance", "Weight management"]},
            "elderly": {"rating": "Recommended", "tips": ["Prevents muscle loss", "Easy to chew if tender", "Low fat option"]}
        }
    },
    "egg": {
        "name": "Egg (Boiled)",
        "category": "Protein",
        "image_url": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 78, "carbs": 0.6, "sugars": 0.6,
            "fiber": 0, "protein": 6, "fat": 5,
            "vitamin_c": 0, "potassium": 63, "sodium": 62
        },
        "health_benefits": [
            "Complete protein source",
            "Rich in choline for brain health",
            "Contains essential amino acids",
            "Good source of Vitamin D"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Brain development (choline)", "Growth support", "Easy breakfast option"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Affordable protein", "Brain fuel for studying", "Muscle support"]},
            "adult":   {"rating": "Recommended", "tips": ["Brain health", "Eye health (lutein)", "Monitor cholesterol"]},
            "elderly": {"rating": "Recommended", "tips": ["Easy to prepare and eat", "Vitamin D source", "Moderate intake advised"]}
        }
    },
    "salmon": {
        "name": "Salmon",
        "category": "Protein",
        "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 208, "carbs": 0, "sugars": 0,
            "fiber": 0, "protein": 20, "fat": 13,
            "vitamin_c": 0, "potassium": 363, "sodium": 59
        },
        "health_benefits": [
            "Rich in Omega-3 fatty acids",
            "Supports brain and heart health",
            "Anti-inflammatory properties",
            "Excellent source of Vitamin D"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Recommended", "tips": ["Brain development (DHA)", "Bone growth (Vitamin D)", "Watch for bones"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Brain function for studying", "Skin health", "Mood regulation"]},
            "adult":   {"rating": "Highly Recommended", "tips": ["Heart disease prevention", "Anti-inflammatory", "Brain health"]},
            "elderly": {"rating": "Highly Recommended", "tips": ["Heart protection", "Joint inflammation relief", "Cognitive support"]}
        }
    },

    # === GRAINS / CARBS ===
    "rice": {
        "name": "White Rice (Cooked)",
        "category": "Grain",
        "image_url": "https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 206, "carbs": 45, "sugars": 0,
            "fiber": 0.6, "protein": 4.3, "fat": 0.4,
            "vitamin_c": 0, "potassium": 55, "sodium": 1
        },
        "health_benefits": [
            "Quick source of energy",
            "Easy to digest",
            "Gluten-free grain",
            "Pairs well with nutrient-rich foods"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Recommended", "tips": ["Energy for activity", "Easy to eat", "Pair with vegetables"]},
            "teen":    {"rating": "Recommended", "tips": ["Energy for sports", "Affordable staple", "Balance with protein"]},
            "adult":   {"rating": "Moderate", "tips": ["High glycemic index", "Control portions", "Choose brown rice if possible"]},
            "elderly": {"rating": "Moderate", "tips": ["Easy to digest", "Watch blood sugar", "Moderate portions"]}
        }
    },
    "bread": {
        "name": "White Bread",
        "category": "Grain",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 79, "carbs": 15, "sugars": 1.6,
            "fiber": 0.6, "protein": 2.7, "fat": 1,
            "vitamin_c": 0, "potassium": 37, "sodium": 147
        },
        "health_benefits": [
            "Quick energy source",
            "Convenient and versatile",
            "Often fortified with vitamins",
            "Low fat content"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Moderate", "tips": ["Easy to eat", "Low nutrition value", "Prefer whole wheat"]},
            "teen":    {"rating": "Moderate", "tips": ["Convenient snack", "Low fiber", "Choose whole grain"]},
            "adult":   {"rating": "Not Recommended", "tips": ["High glycemic index", "Low fiber", "Switch to whole grain"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Spikes blood sugar", "Low nutrition", "Choose whole wheat"]}
        }
    },

    # === FAST FOOD / UNHEALTHY ===
    "french_fries": {
        "name": "French Fries",
        "category": "Fast Food",
        "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 365, "carbs": 44, "sugars": 0.3,
            "fiber": 3.8, "protein": 4, "fat": 17,
            "vitamin_c": 7, "potassium": 579, "sodium": 246
        },
        "health_benefits": [
            "Source of potassium (from potato)",
            "Provides quick energy",
            "Contains some Vitamin C",
            "Minimal other health benefits"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Not Recommended", "tips": ["High in unhealthy fats", "Risk of obesity", "Limit intake"]},
            "teen":    {"rating": "Not Recommended", "tips": ["Contributes to acne", "Weight gain risk", "Choose baked instead"]},
            "adult":   {"rating": "Not Recommended", "tips": ["Heart disease risk", "High sodium", "Weight gain"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Blood pressure risk", "Hard to digest", "Avoid regularly"]}
        }
    },
    "burger": {
        "name": "Cheeseburger",
        "category": "Fast Food",
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 535, "carbs": 40, "sugars": 10,
            "fiber": 1.5, "protein": 28, "fat": 28,
            "vitamin_c": 2, "potassium": 330, "sodium": 1108
        },
        "health_benefits": [
            "Good source of protein",
            "Contains iron and zinc",
            "Provides B vitamins from beef",
            "High calorie – not ideal for regular consumption"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Not Recommended", "tips": ["Very high in sodium", "Too calorie-dense", "Occasional treat only"]},
            "teen":    {"rating": "Not Recommended", "tips": ["Excess calories", "Acne trigger", "Limit to once a week"]},
            "adult":   {"rating": "Not Recommended", "tips": ["Heart disease risk", "High sodium & fat", "Choose lean alternatives"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Blood pressure danger", "Hard to digest", "Avoid if possible"]}
        }
    },
    "pizza": {
        "name": "Pizza (Cheese)",
        "category": "Fast Food",
        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 266, "carbs": 33, "sugars": 3.6,
            "fiber": 2.3, "protein": 11, "fat": 10,
            "vitamin_c": 1, "potassium": 172, "sodium": 598
        },
        "health_benefits": [
            "Source of calcium from cheese",
            "Contains protein",
            "Provides some carbohydrates for energy",
            "High in sodium and saturated fat"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Moderate", "tips": ["Calcium from cheese", "High sodium", "Limit to 1-2 slices"]},
            "teen":    {"rating": "Moderate", "tips": ["Convenient meal", "High calories", "Add veggie toppings"]},
            "adult":   {"rating": "Not Recommended", "tips": ["High sodium", "Saturated fat risk", "Eat sparingly"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Blood pressure concern", "Hard to digest", "Choose healthier options"]}
        }
    },
    "hotdog": {
        "name": "Hotdog",
        "category": "Fast Food",
        "image_url": "https://images.unsplash.com/photo-1612392062422-ef19b42f74df?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 290, "carbs": 24, "sugars": 4,
            "fiber": 0.8, "protein": 10, "fat": 17,
            "vitamin_c": 0, "potassium": 180, "sodium": 810
        },
        "health_benefits": [
            "Source of protein",
            "Quick meal option",
            "Contains B vitamins",
            "Highly processed – minimal health benefits"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Not Recommended", "tips": ["Choking hazard if not cut", "Highly processed", "Preservatives concern"]},
            "teen":    {"rating": "Not Recommended", "tips": ["Processed meat risk", "High sodium", "Choose healthier protein"]},
            "adult":   {"rating": "Not Recommended", "tips": ["Linked to cancer risk", "Very high sodium", "Avoid regular consumption"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Processed meat dangers", "Blood pressure risk", "Avoid entirely"]}
        }
    },

    # === DRINKS ===
    "milk": {
        "name": "Whole Milk",
        "category": "Dairy",
        "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 149, "carbs": 12, "sugars": 12,
            "fiber": 0, "protein": 8, "fat": 8,
            "vitamin_c": 0, "potassium": 322, "sodium": 105
        },
        "health_benefits": [
            "Excellent source of calcium",
            "Supports bone health",
            "Good protein source",
            "Contains Vitamin D (if fortified)"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Highly Recommended", "tips": ["Essential for bone growth", "Calcium source", "Protein for growth"]},
            "teen":    {"rating": "Highly Recommended", "tips": ["Peak bone building years", "Muscle recovery", "Brain health"]},
            "adult":   {"rating": "Recommended", "tips": ["Bone maintenance", "Choose low-fat if needed", "Protein source"]},
            "elderly": {"rating": "Recommended", "tips": ["Prevents osteoporosis", "Choose low-fat", "Check lactose tolerance"]}
        }
    },
    "soda": {
        "name": "Soda (Cola)",
        "category": "Beverage",
        "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 140, "carbs": 39, "sugars": 39,
            "fiber": 0, "protein": 0, "fat": 0,
            "vitamin_c": 0, "potassium": 0, "sodium": 45
        },
        "health_benefits": [
            "No significant health benefits",
            "Provides quick sugar energy (temporary)",
            "High risk of tooth decay",
            "Linked to obesity and diabetes"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Not Recommended", "tips": ["Tooth decay risk", "Obesity risk", "Replace with water or juice"]},
            "teen":    {"rating": "Not Recommended", "tips": ["Empty calories", "Acne trigger", "Choose water instead"]},
            "adult":   {"rating": "Not Recommended", "tips": ["Diabetes risk", "Weight gain", "Zero nutrition"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Blood sugar spike", "Bone density loss", "Avoid completely"]}
        }
    },

    # === SNACKS ===
    "chips": {
        "name": "Potato Chips",
        "category": "Snack",
        "image_url": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=500&q=60",
        "nutrition": {
            "calories": 152, "carbs": 15, "sugars": 0.1,
            "fiber": 1.2, "protein": 2, "fat": 10,
            "vitamin_c": 3, "potassium": 362, "sodium": 170
        },
        "health_benefits": [
            "Some potassium from potato",
            "Quick snack energy",
            "High in sodium and fat",
            "Minimal nutritional value"
        ],
        "age_sensitivity": {
            "kid":     {"rating": "Not Recommended", "tips": ["High sodium for small bodies", "Habit-forming snack", "Choose fruit instead"]},
            "teen":    {"rating": "Not Recommended", "tips": ["Empty calories", "Skin issues", "Replace with nuts"]},
            "adult":   {"rating": "Not Recommended", "tips": ["High sodium", "Trans fat risk", "Weight gain"]},
            "elderly": {"rating": "Not Recommended", "tips": ["Blood pressure risk", "Low nutrition", "Avoid salty snacks"]}
        }
    },
}


import os
import csv

# Path to the Kaggle CSV files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_kaggle_food(food_name):
    """
    Search for a food item in the Kaggle CSV files and return a formatted dictionary.
    """
    food_name = food_name.lower().strip()
    
    csv_files = [
        'FOOD-DATA-GROUP1.csv',
        'FOOD-DATA-GROUP2.csv',
        'FOOD-DATA-GROUP3.csv',
        'FOOD-DATA-GROUP4.csv',
        'FOOD-DATA-GROUP5.csv'
    ]

    # Phase 1: Search ALL files for an Exact Match (Priority)
    for filename in csv_files:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path): continue
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['food'].lower().strip() == food_name:
                        return format_kaggle_row(row)
        except Exception: continue

    # Phase 2: Search ALL files for a Whole Word Match (Fallback)
    for filename in csv_files:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path): continue
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row_food = row['food'].lower()
                    if f" {food_name} " in f" {row_food} ":
                        return format_kaggle_row(row)
        except Exception: continue
                    
    return None

def format_kaggle_row(row):
    """Converts a CSV row into the SnapEat food object format."""
    try:
        # Some CSVs might have slightly different headers or empty values
        # Default to 0 for nutrition values if missing/empty
        def safe_float(val):
            try: return float(val) if val and val.strip() else 0.0
            except: return 0.0

        return {
            "name": row['food'].title(),
            "category": "General",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=60",
            "nutrition": {
                "calories": safe_float(row.get('Caloric Value', 0)),
                "carbs": safe_float(row.get('Carbohydrates', 0)),
                "sugars": safe_float(row.get('Sugars', 0)),
                "fiber": safe_float(row.get('Dietary Fiber', 0)),
                "protein": safe_float(row.get('Protein', 0)),
                "fat": safe_float(row.get('Fat', 0)),
                "vitamin_c": safe_float(row.get('Vitamin C', 0)),
                "potassium": safe_float(row.get('Potassium', 0)),
                "sodium": safe_float(row.get('Sodium', 0))
            },
            "health_benefits": [
                "Contains nutrients found in " + row['food'],
                "Provides energy (" + row.get('Caloric Value', '0') + " kcal)",
                "Contains " + row.get('Protein', '0') + "g of protein"
            ],
            "age_sensitivity": {
                "kid":     {"rating": "Safe", "tips": ["Check for allergens", "Serve in small portions"]},
                "teen":    {"rating": "Safe", "tips": ["Good for growth", "Nutrient dense"]},
                "adult":   {"rating": "Safe", "tips": ["Maintain balanced diet", "Watch calories"]},
                "elderly": {"rating": "Safe", "tips": ["Easy to digest", "High in minerals"]}
            }
        }
    except Exception as e:
        print(f"Error formatting row: {e}")
        return None


def get_food_by_name(food_name):
    """Look up a food item by name (Dictionary first, then Kaggle CSV)."""
    if not food_name: return None
    
    query = food_name.lower().strip().replace("_", " ") # Normalize to spaces for better matching
    query_id = query.replace(" ", "_")

    # 1. Check Manual Dictionary (Exact match)
    if query_id in FOOD_DATABASE:
        return FOOD_DATABASE[query_id]

    # 2. Check Manual Dictionary (Whole word and plural/singular matching)
    for key, data in FOOD_DATABASE.items():
        key_name = data["name"].lower()
        # Direct word match or singular/plural check (e.g., strawberry vs strawberries)
        is_plural_match = (query + "s" == key) or (query + "es" == key) or (key + "s" == query) or (key + "es" == query)
        # Handle 'y' to 'ies' cases
        if not is_plural_match and query.endswith('y'):
            is_plural_match = (query[:-1] + "ies" == key)
        if not is_plural_match and key.endswith('ies'):
            is_plural_match = (key[:-3] + "y" == query)
        
        if f" {query} " in f" {key_name} " or f" {key_name} " in f" {query} " or is_plural_match:
            return data

    # 3. Fallback to Kaggle CSVs
    # We search with the space-normalized name
    kaggle_result = load_kaggle_food(query)
    if kaggle_result:
        return kaggle_result

    # 4. FINAL DYNAMIC FALLBACK: If food not in DB or CSV, create a "General" profile
    return {
        "name": food_name.title(),
        "category": "General",
        "image_url": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=500&q=80",
        "nutrition": {
            "calories": 100, "carbs": 15, "sugars": 8, "fiber": 3, "protein": 2, "fat": 1
        },
        "health_benefits": [
            "Provides essential energy",
            "Contains natural vitamins and minerals",
            "Part of a balanced diet"
        ],
        "age_sensitivity": {
            "kid": {"rating": "Good", "tips": ["Always wash fresh produce", "Balanced nutrition"]},
            "teen": {"rating": "Good", "tips": ["Steady energy source"]},
            "adult": {"rating": "Good", "tips": ["Part of a healthy lifestyle"]},
            "elderly": {"rating": "Good", "tips": ["Easy to digest"]}
        }
    }


def get_all_food_names():
    """Return a list of food names (static names only)."""
    return [data["name"] for data in FOOD_DATABASE.values()]


def search_foods(query):
    """Search for foods matching a query string."""
    query = query.lower().strip()
    results = []
    
    # Static database search
    for key, data in FOOD_DATABASE.items():
        if query in key or query in data["name"].lower() or query in data["category"].lower():
            results.append(data)
    
    # If few results, try CSV (limit to 1 result for speed)
    if len(results) < 3:
        csv_item = load_kaggle_food(query)
        if csv_item and csv_item["name"] not in [r["name"] for r in results]:
            results.append(csv_item)
            
    return results
