"""Home page view implemented with Django templates (PR6)."""
from django.shortcuts import render

from web_data import get_catalog


def index(request):
    """Display the current counts from JSON-backed domain objects."""
    users, recipes, experiments = get_catalog()
    return render(
        request,
        "homepage/index.html",
        {
            "page_title": "Главная",
            "users_count": len(users),
            "recipes_count": len(recipes),
            "experiments_count": len(experiments),
            "latest": experiments[-3:][::-1],
        },
    )
