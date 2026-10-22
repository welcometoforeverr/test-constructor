"""Recipe views backed by parameterized SQLite queries (PR7)."""
from django.shortcuts import render

from db.queries import (
    list_recipes,
    recipe_categories,
    recipe_detail as get_recipe_detail,
)


def recipe_list(request):
    """Show recipes from SQLite with search and category filtering."""
    search = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    return render(
        request,
        "recipes/recipe_list.html",
        {
            "page_title": "Рецепты",
            "recipes": list_recipes(search, category),
            "query": search,
            "category": category,
        },
    )


def recipe_detail(request, recipe_id: int):
    """Show one SQLite recipe row or return HTTP 404."""
    recipe = get_recipe_detail(recipe_id)
    return render(
        request,
        "recipes/recipe_detail.html",
        {"page_title": "Рецепт", "recipe": recipe},
        status=404 if recipe is None else 200,
    )


def category_statistics(request):
    """Show GROUP BY statistics for recipe categories."""
    return render(
        request,
        "recipes/category_stats.html",
        {
            "page_title": "Категории рецептов",
            "categories": recipe_categories(),
        },
    )
