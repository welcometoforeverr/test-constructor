"""Recipe pages using migrated models and ORM aggregation."""

from django.shortcuts import render

from .queries import recipe_catalog, recipe_categories


def recipe_list(request):
    search = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    return render(
        request,
        "recipes/recipe_list.html",
        {
            "page_title": "Рецепты",
            "recipes": recipe_catalog(search, category),
            "query": search,
            "category": category,
        },
    )


def recipe_detail(request, recipe_id):
    recipe = recipe_catalog().filter(pk=recipe_id).first()
    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "page_title": "Рецепт",
            "recipe": recipe,
        },
        status=404 if recipe is None else 200,
    )


def category_statistics(request):
    return render(
        request,
        "recipes/category_stats.html",
        {
            "page_title": "Категории рецептов",
            "categories": recipe_categories(),
        },
    )
