"""
Food identification and nutrition retrieval module.
Uses the local food_dataset to look up food items and their nutritional data.
"""

from backend.food_dataset import get_food_by_name, search_foods, get_all_food_names


def identify_food_item(image_data=None, food_name=None):
    """
    Identify a food item by name lookup against the dataset.
    In a production system, this would use an ML model on image_data.

    Args:
        image_data: Raw image bytes (reserved for future ML integration).
        food_name: Text name of the food to look up.

    Returns:
        dict with food data or None if not found.
    """
    if food_name:
        result = get_food_by_name(food_name)
        if result:
            return {
                "status": "identified",
                "food": result
            }

    # If image_data is provided but no food_name, return placeholder
    # for future ML model integration
    if image_data:
        return {
            "status": "pending_ml",
            "message": "Image received. ML model integration pending."
        }

    return None


def get_nutrition_data(food_name):
    """
    Retrieve nutritional values (calories, protein, fats, etc.)
    from the local food dataset.

    Args:
        food_name: Name of the food item.

    Returns:
        dict with nutrition data, or None if not found.
    """
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
    """
    Search for food items matching a query.

    Args:
        query: Search string.

    Returns:
        List of matching food summaries.
    """
    results = search_foods(query)
    return [
        {
            "name": item["name"],
            "category": item["category"],
            "calories": item["nutrition"]["calories"]
        }
        for item in results
    ]


def get_available_foods():
    """Return all available food names in the dataset."""
    return get_all_food_names()
