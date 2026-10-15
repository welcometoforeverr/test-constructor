"""Read-only recipe views with Django templates (PR6)."""
from django.shortcuts import render

from web_data import get_recipes


def recipe_list(request):
    """Show recipes loaded from the existing JSON domain store."""
    recipes = get_recipes()
    query = request.GET.get("q", "").strip()
    if query:
        recipes = [
            item for item in recipes
            if query.lower() in item.name.lower()
        ]
    return render(
        request,
        "recipes/recipe_list.html",
        {
            "page_title": "Рецепты",
            "recipes": sorted(recipes, key=lambda item: item.name.lower()),
            "query": query,
        },
    )


def recipe_detail(request, recipe_id: int):
    """Show recipe details; missing IDs return 404 with a rendered template."""
    recipe = next(
        (item for item in get_recipes() if item.id == recipe_id),
        None,
    )
    return render(
        request,
        "recipes/recipe_detail.html",
        {"page_title": "Рецепт", "recipe": recipe},
        status=404 if recipe is None else 200,
    )
