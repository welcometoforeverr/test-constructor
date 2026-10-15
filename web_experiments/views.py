"""Read-only experiment views using the domain object graph (PR6)."""
from django.shortcuts import render

from web_data import get_catalog


def experiment_list(request):
    """Display every recorded experiment and its state."""
    _, _, experiments = get_catalog()
    return render(
        request,
        "experiments/experiment_list.html",
        {
            "page_title": "Эксперименты",
            "experiments": sorted(
                experiments, key=lambda item: item.id, reverse=True
            ),
        },
    )


def experiment_detail(request, experiment_id: int):
    """Show one experiment or a styled 404 response."""
    _, _, experiments = get_catalog()
    experiment = next(
        (item for item in experiments if item.id == experiment_id),
        None,
    )
    return render(
        request,
        "experiments/experiment_detail.html",
        {"page_title": "Эксперимент", "experiment": experiment},
        status=404 if experiment is None else 200,
    )
