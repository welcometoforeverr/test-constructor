"""Home page backed by SQLite queries (PR7)."""
from django.shortcuts import render

from db.queries import dashboard_stats, list_experiments


def index(request):
    """Display SQLite-backed counters and latest experiments."""
    stats = dashboard_stats()
    return render(
        request,
        "homepage/index.html",
        {
            "page_title": "Главная",
            **stats,
            "latest": list_experiments()[:3],
        },
    )
