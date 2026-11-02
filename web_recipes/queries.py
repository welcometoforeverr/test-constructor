"""Recipe queries shared by list, detail, statistics and the home page."""

from django.db.models import Avg, Count
from django.db.models.functions import Round

from .models import Recipe


def recipe_catalog(search="", category=""):
    recipes = Recipe.objects.annotate(
        experiments_count=Count("experiments"),
        average_score=Round(Avg("experiments__result__taste_score"), 2),
    )
    if search:
        recipes = recipes.filter(name__icontains=search)
    if category:
        recipes = recipes.filter(category__icontains=category)
    return recipes.order_by("name", "id")


def recipe_categories():
    return (
        Recipe.objects.order_by()
        .values("category")
        .annotate(recipes_count=Count("id"))
        .order_by("-recipes_count", "category")
    )
