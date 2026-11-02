"""Search, filtering, ordering and pagination of ORM objects."""

from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import ExperimentFilterForm
from .models import Experiment
from .queries import experiment_catalog, experiment_statistics


def experiment_list(request):
    form = ExperimentFilterForm(request.GET)
    form.is_valid()
    # Valid fields remain usable even if another field has an input error.
    experiments = experiment_catalog(form.cleaned_data)
    page = Paginator(experiments, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "experiments/experiment_list.html",
        {
            "page_title": "Эксперименты",
            "experiments": page,
            "page_obj": page,
            "filter_form": form,
        },
    )


def experiment_detail(request, experiment_id):
    experiment = (
        Experiment.objects.select_related("recipe", "user", "result")
        .filter(pk=experiment_id)
        .first()
    )
    return render(
        request,
        "experiments/experiment_detail.html",
        {
            "page_title": "Эксперимент",
            "experiment": experiment,
        },
        status=404 if experiment is None else 200,
    )


def statistics(request):
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
