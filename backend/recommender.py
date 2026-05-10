"""
Recommendation engine for SnapEat.
Suggests healthier alternatives and provides age-specific dietary advice.
"""

from backend.food_dataset import FOOD_DATABASE
from backend.analyzer import get_food_by_name, get_available_foods
# FOOD_DATABASE replaced by AI calls
from backend.classifier import calculate_health_score


def get_recommendations(food_name, health_status=None):
    """
    Suggest healthier alternatives using AI.
    """
    from backend.analyzer import get_model
    model = get_model()
    if not model: return []

    try:
        prompt = f"Given the food '{food_name}', suggest 3 healthier alternatives. Return ONLY a JSON list of objects with: name, reason_why_healthier."
        response = model.generate_content(prompt)
        import json
        raw_text = response.text.strip()
        if "```" in raw_text:
            start = raw_text.find("[")
            end = raw_text.rfind("]") + 1
            raw_text = raw_text[start:end]
        
        alts = json.loads(raw_text)
        # Format for template
        recommendations = []
        for alt in alts:
            recommendations.append({
                "name": alt["name"],
                "category": "Recommended",
                "health_score": 9,
                "reason": alt.get("reason_why_healthier", "Better nutritional profile"),
                "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=500&q=60"
            })
        return recommendations
    except:
        return []


def get_household_suggestions(member_type):
    """
    Provide food suggestions tailored for specific household members.

    Args:
        member_type: One of 'kid', 'teen', 'adult', 'elderly'.

    Returns:
        list of dicts with food suggestions for the specified age group.
    """
    member_type = member_type.lower().strip()
    valid_types = ["kid", "teen", "adult", "elderly"]

    if member_type not in valid_types:
        return []

    suggestions = []

    for key, food in FOOD_DATABASE.items():
        age_data = food.get("age_sensitivity", {}).get(member_type, {})
        rating = age_data.get("rating", "")

        if rating == "Highly Recommended":
            suggestions.append({
                "name": food["name"],
                "category": food["category"],
                "rating": rating,
                "tips": age_data.get("tips", []),
                "calories": food["nutrition"]["calories"],
                "image_url": food.get("image_url", "")
            })

    # Sort by calorie count (lower first for healthier options)
    suggestions.sort(key=lambda x: x["calories"])

    return suggestions


def get_meal_plan_suggestions(member_type=None):
    """
    Generate a simple daily meal plan based on age group.

    Args:
        member_type: Optional age group filter.

    Returns:
        dict with breakfast, lunch, dinner suggestions.
    """
    all_foods = list(FOOD_DATABASE.values())

    # Categorize foods
    fruits = [f for f in all_foods if f["category"] == "Fruit"]
    proteins = [f for f in all_foods if f["category"] == "Protein"]
    veggies = [f for f in all_foods if f["category"] == "Vegetable"]
    grains = [f for f in all_foods if f["category"] == "Grain"]

    def pick_best(food_list, member_type=None):
        """Pick the best food from a list based on health score and age suitability."""
        if not food_list:
            return None

        scored = []
        for food in food_list:
            score = calculate_health_score(food["nutrition"])
            if member_type:
                age_data = food.get("age_sensitivity", {}).get(member_type, {})
                if age_data.get("rating") == "Highly Recommended":
                    score += 3
                elif age_data.get("rating") == "Recommended":
                    score += 1
            scored.append((food, score))

        scored.sort(key=lambda x: -x[1])
        return scored[0][0]["name"] if scored else None

    return {
        "breakfast": {
            "protein": pick_best(proteins, member_type),
            "fruit": pick_best(fruits, member_type),
            "dairy": pick_best([f for f in all_foods if f["category"] == "Dairy"], member_type)
        },
        "lunch": {
            "protein": pick_best(proteins, member_type),
            "vegetable": pick_best(veggies, member_type),
            "grain": pick_best(grains, member_type)
        },
        "dinner": {
            "protein": pick_best(proteins, member_type),
            "vegetable": pick_best(veggies, member_type),
            "fruit": pick_best(fruits, member_type)
        }
    }
