"""
Recommendation engine for SnapEat.
Suggests healthier alternatives and provides age-specific dietary advice.
"""

from backend.food_dataset import FOOD_DATABASE, get_food_by_name
from backend.classifier import calculate_health_score


def get_recommendations(food_name, health_status=None):
    """
    Suggest healthier alternatives if the food is classified as 'Unhealthy' or 'Moderate'.

    Args:
        food_name: Name of the current food item.
        health_status: Optional health classification string.

    Returns:
        list of dicts with recommended food alternatives.
    """
    current_food = get_food_by_name(food_name)
    if not current_food:
        return []

    current_score = calculate_health_score(current_food["nutrition"])
    current_category = current_food["category"]

    recommendations = []

    for key, food in FOOD_DATABASE.items():
        # Skip the same food
        if food["name"] == current_food["name"]:
            continue

        food_score = calculate_health_score(food["nutrition"])

        # Only recommend foods with a better health score
        if food_score > current_score:
            recommendations.append({
                "name": food["name"],
                "category": food["category"],
                "health_score": food_score,
                "calories": food["nutrition"]["calories"],
                "image_url": food.get("image_url", ""),
                "same_category": food["category"] == current_category
            })

    # Sort: same category first, then by health score descending
    recommendations.sort(key=lambda x: (-x["same_category"], -x["health_score"]))

    # Return top 5
    return recommendations[:5]


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
