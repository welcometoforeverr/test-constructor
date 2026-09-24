from models import Recipe
from recipes import (
    add_recipe,
    filter_recipes_by_category,
    find_recipes,
    sort_recipes,
)


def test_add_recipe_returns_object() -> None:
    recipes: list[Recipe] = []
    recipe = add_recipe(recipes, "Сырники", "Завтрак")
    assert isinstance(recipe, Recipe)
    assert recipe.id == 1


def test_find_filter_and_sort() -> None:
    recipes = [
        Recipe(1, "Шоколадный кекс", "Выпечка"),
        Recipe(2, "Блины", "Завтрак"),
    ]
    assert find_recipes(recipes, "кекс")[0].id == 1
    assert list(filter_recipes_by_category(recipes, "завтрак"))[0].id == 2
    assert sort_recipes(recipes)[0].name == "Блины"
