"""Search, filtering, ordering and pagination of ORM objects."""

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import ExperimentFilterForm, ExperimentForm
from .models import Experiment, ExperimentResult
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
        Experiment.objects.with_details()
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


@transaction.atomic
def save_experiment_form(form):
    experiment = form.save()
    score = form.cleaned_data["taste_score"]
    ExperimentResult.objects.update_or_create(
        experiment=experiment,
        defaults={
            "taste_score": score,
            "status": ExperimentResult.outcome_for_score(score),
        },
    )
    return experiment


@require_http_methods(["GET", "POST"])
def experiment_create(request):
    form = ExperimentForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        experiment = save_experiment_form(form)
        return redirect("experiments:detail", experiment_id=experiment.pk)
    return render(
        request, "includes/edit_form.html",
        {"form": form, "heading": "Новый эксперимент", "back_url": "experiments:list"},
    )


@require_http_methods(["GET", "POST"])
def experiment_edit(request, experiment_id):
    experiment = get_object_or_404(Experiment.objects.with_details(), pk=experiment_id)
    form = ExperimentForm(
        request.POST if request.method == "POST" else None, instance=experiment
    )
    if request.method == "POST" and form.is_valid():
        experiment = save_experiment_form(form)
        return redirect("experiments:detail", experiment_id=experiment.pk)
    return render(
        request, "includes/edit_form.html",
        {"form": form, "heading": "Редактировать эксперимент",
         "back_url": "experiments:list"},
    )


@require_POST
def experiment_cancel(request, experiment_id):
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    experiment.cancel()
    return redirect("experiments:detail", experiment_id=experiment.pk)
