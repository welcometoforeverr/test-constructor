"""Functions for working with recipes."""


def add_recipe(
    recipes: list[dict],
    name: str,
    category: str,
) -> dict:
    """Add a recipe to the collection and return the created record."""
    cleaned_name = name.strip()
    cleaned_category = category.strip()
    if len(cleaned_name) < 3:
        raise ValueError("Название рецепта должно содержать минимум 3 символа")
    if not cleaned_category:
        raise ValueError("Категория рецепта не может быть пустой")

    recipe = {
        "id": max((item["id"] for item in recipes), default=0) + 1,
        "name": cleaned_name,
        "category": cleaned_category,
    }
    recipes.append(recipe)
    return recipe


def find_recipes(recipes: list[dict], query: str) -> list[dict]:
    """Find recipes whose names contain the requested substring."""
    normalized_query = query.strip().lower()
    return [
        recipe
        for recipe in recipes
        if normalized_query in recipe["name"].lower()
    ]


def filter_recipes_by_category(
    recipes: list[dict],
    category: str,
):
    """Yield recipes belonging to the specified category."""
    normalized_category = category.strip().lower()
    for recipe in recipes:
        if recipe["category"].lower() == normalized_category:
            yield recipe


def sort_recipes(recipes: list[dict]) -> list[dict]:
    """Return recipes sorted alphabetically by name."""
    return sorted(recipes, key=lambda recipe: recipe["name"].lower())
