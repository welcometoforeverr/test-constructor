from recipes import (
    add_recipe,
    filter_recipes_by_category,
    find_recipes,
    sort_recipes,
)


def test_add_recipe() -> None:
    recipes = []
    recipe = add_recipe(recipes, "Сырники", "Завтрак")
    assert recipe["id"] == 1
    assert recipes[0]["name"] == "Сырники"


def test_find_and_filter_recipes() -> None:
    recipes = [
        {"id": 1, "name": "Шоколадный кекс", "category": "Выпечка"},
        {"id": 2, "name": "Томатный соус", "category": "Соусы"},
    ]
    assert find_recipes(recipes, "кекс")[0]["id"] == 1
    assert list(filter_recipes_by_category(recipes, "соусы"))[0]["id"] == 2


def test_sort_recipes() -> None:
    recipes = [
        {"id": 1, "name": "Шоколадный кекс", "category": "Выпечка"},
        {"id": 2, "name": "Блины", "category": "Завтрак"},
    ]
    assert sort_recipes(recipes)[0]["name"] == "Блины"
