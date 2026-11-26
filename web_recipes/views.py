"""Recipe pages using migrated models and ORM aggregation."""

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import Recipe

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


def recipe_slug_detail(request, slug):
    recipe = recipe_catalog().filter(slug=slug).first()
    return render(
        request,
        "recipes/recipe_detail.html",
        {"page_title": "Рецепт", "recipe": recipe},
        status=404 if recipe is None else 200,
    )


@require_http_methods(["GET", "POST"])
def recipe_create(request):
    form = RecipeForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
    )
    if request.method == "POST" and form.is_valid():
        return redirect(form.save())
    return render(
        request, "includes/edit_form.html",
        {"form": form, "heading": "Добавить рецепт", "back_url": "recipes:list"},
    )


@require_http_methods(["GET", "POST"])
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = RecipeForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
        instance=recipe,
    )
    if request.method == "POST" and form.is_valid():
        return redirect(form.save())
    return render(
        request, "includes/edit_form.html",
        {"form": form, "heading": "Редактировать рецепт", "back_url": "recipes:list"},
    )
