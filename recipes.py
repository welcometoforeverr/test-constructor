"""Collection operations for Recipe objects."""

from models import Recipe


def add_recipe(recipes: list[Recipe], name: str, category: str) -> Recipe:
    """Create a Recipe object and add it to the collection."""
    recipe_id = max((recipe.id for recipe in recipes), default=0) + 1
    recipe = Recipe(recipe_id, name, category)
    recipes.append(recipe)
    return recipe


def find_recipes(recipes: list[Recipe], query: str) -> list[Recipe]:
    """Find recipes by name substring."""
    normalized = query.strip().lower()
    return [recipe for recipe in recipes if normalized in recipe.name.lower()]


def filter_recipes_by_category(
    recipes: list[Recipe],
    category: str,
):
    """Yield recipes from the requested category."""
    normalized = category.strip().lower()
    for recipe in recipes:
        if recipe.category.lower() == normalized:
            yield recipe


def sort_recipes(recipes: list[Recipe]) -> list[Recipe]:
    """Return recipes sorted by name."""
    return sorted(recipes, key=lambda recipe: recipe.name.lower())
