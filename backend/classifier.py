"""
Health classification module.
Classifies food items as Healthy, Moderate, or Unhealthy
and calculates a health score (1-10) based on nutritional data.
"""

from backend.food_dataset import get_food_by_name


# Thresholds for health scoring
SCORING_RULES = {
    "calories":  {"good": 150, "moderate": 300},   # per serving
    "sugars":    {"good": 10,  "moderate": 20},     # grams
    "fiber":     {"good": 3,   "moderate": 1},      # grams (higher = better)
    "protein":   {"good": 10,  "moderate": 5},      # grams (higher = better)
    "fat":       {"good": 5,   "moderate": 15},     # grams
    "sodium":    {"good": 200, "moderate": 500},    # mg
}


def classify_health_status(nutrition_data):
    """
    Categorize food as Healthy, Moderate, or Unhealthy
    based on nutritional profile.

    Args:
        nutrition_data: dict with keys like calories, sugars, fat, etc.

    Returns:
        str: "Healthy", "Moderate", or "Unhealthy"
    """
    score = calculate_health_score(nutrition_data)

    if score >= 7:
        return "Healthy"
    elif score >= 4:
        return "Moderate"
    else:
        return "Unhealthy"


def calculate_health_score(nutrition_data):
    """
    Return a score between 1 and 10 based on nutritional quality.

    Scoring breakdown:
    - Lower calories, sugars, fat, sodium = higher score
    - Higher fiber, protein = higher score

    Args:
        nutrition_data: dict with nutritional values.

    Returns:
        int: Score from 1 to 10.
    """
    if not nutrition_data:
        return 5  # neutral default

    points = 0
    max_points = 0

    # --- Lower is better metrics ---
    for metric in ["calories", "sugars", "fat", "sodium"]:
        value = nutrition_data.get(metric, 0)
        good = SCORING_RULES[metric]["good"]
        moderate = SCORING_RULES[metric]["moderate"]
        max_points += 2

        if value <= good:
            points += 2
        elif value <= moderate:
            points += 1
        # else: 0 points

    # --- Higher is better metrics ---
    for metric in ["fiber", "protein"]:
        value = nutrition_data.get(metric, 0)
        good = SCORING_RULES[metric]["good"]
        moderate = SCORING_RULES[metric]["moderate"]
        max_points += 2

        if value >= good:
            points += 2
        elif value >= moderate:
            points += 1
        # else: 0 points

    # Scale to 1-10
    if max_points == 0:
        return 5

    raw_score = (points / max_points) * 10
    return max(1, min(10, round(raw_score)))


def get_full_classification(food_name):
    """
    Get complete health classification for a food item.

    Args:
        food_name: Name of the food.

    Returns:
        dict with health_status, health_score, and age_sensitivity, or None.
    """
    food = get_food_by_name(food_name)
    if not food:
        return None

    nutrition = food["nutrition"]
    return {
        "name": food["name"],
        "health_status": classify_health_status(nutrition),
        "health_score": calculate_health_score(nutrition),
        "age_sensitivity": food.get("age_sensitivity", {})
    }
