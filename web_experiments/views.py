"""Experiment views backed by SQLite JOIN queries (PR7)."""
from django.shortcuts import render

from db.queries import (
    experiment_detail as get_experiment_detail,
    experiment_statistics,
    list_experiments,
)


def _score_param(raw_value: str) -> int:
    """Convert min_score parameter to the safe range from 1 to 10."""
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return 1
    return min(max(value, 1), 10)


def experiment_list(request):
    """Display joined experiment data filtered by a parameterized WHERE."""
    min_score = _score_param(request.GET.get("min_score", "1"))
    return render(
        request,
        "experiments/experiment_list.html",
        {
            "page_title": "Эксперименты",
            "experiments": list_experiments(min_score),
            "min_score": min_score,
        },
    )


def experiment_detail(request, experiment_id: int):
    """Show one joined SQLite row or return HTTP 404."""
    experiment = get_experiment_detail(experiment_id)
    return render(
        request,
        "experiments/experiment_detail.html",
        {"page_title": "Эксперимент", "experiment": experiment},
        status=404 if experiment is None else 200,
    )


def statistics(request):
    """Display aggregate and GROUP BY experiment statistics."""
    overall, by_recipe, by_status = experiment_statistics()
    return render(
        request,
        "experiments/statistics.html",
        {
            "page_title": "Статистика",
            "overall": overall,
            "by_recipe": by_recipe,
            "by_status": by_status,
        },
    )
