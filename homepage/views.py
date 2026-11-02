"""Home page with ORM counters and a limited recent selection."""

from django.shortcuts import render

from web_experiments.queries import dashboard_stats, experiment_catalog


def index(request):
    return render(
        request,
        "homepage/index.html",
        {
            "page_title": "Главная",
            **dashboard_stats(),
            "latest": experiment_catalog({})[:3],
        },
    )
