"""ORM filters and aggregates used by the actual web pages."""

from django.db.models import (
    Avg,
    Case,
    CharField,
    Count,
    F,
    Max,
    Min,
    Q,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Round

from web_recipes.models import Recipe
from .models import Experiment, ExperimentResult, User

SORTS = {
    "newest": ("-experiment_date", "-id"),
    "oldest": ("experiment_date", "id"),
    "score": ("-result__taste_score", "-id"),
    "recipe": ("recipe__name", "-experiment_date", "-id"),
}


def experiment_catalog(params):
    experiments = Experiment.objects.with_details()
    experiments = experiments.filter(
        result__taste_score__gte=params.get("min_score") or 1
    )
    if params.get("q"):
        query = params["q"]
        experiments = experiments.filter(
            Q(change_description__icontains=query)
            | Q(recipe__name__icontains=query)
            | Q(user__name__icontains=query)
        )
    if params.get("recipe"):
        experiments = experiments.filter(recipe=params["recipe"])
    if params.get("user"):
        experiments = experiments.filter(user=params["user"])
    if params.get("date"):
        experiments = experiments.for_date(params["date"])
    if params.get("status") == "active":
        experiments = experiments.active()
    elif params.get("status") == "cancelled":
        experiments = experiments.cancelled()
    return experiments.order_by(*SORTS.get(params.get("sort"), SORTS["newest"]))


def dashboard_stats():
    return {
        "users_count": User.objects.count(),
        "recipes_count": Recipe.objects.count(),
        "experiments_count": Experiment.objects.count(),
        "average_score": ExperimentResult.objects.aggregate(
            value=Round(Avg("taste_score"), 2)
        )["value"],
    }


def experiment_statistics():
    overall = ExperimentResult.objects.aggregate(
        results_count=Count("id"),
        average_score=Round(Avg("taste_score"), 2),
        min_score=Min("taste_score"),
        max_score=Max("taste_score"),
    )
    overall["total_minutes"] = Experiment.objects.aggregate(
        total=Sum("duration_minutes", default=0)
    )["total"]
    by_recipe = Recipe.objects.annotate(
        experiments_count=Count("experiments"),
        average_score=Round(Avg("experiments__result__taste_score"), 2),
    ).order_by("-experiments_count", "name", "id")
    by_status = (
        Experiment.objects.annotate(
            display_status=Case(
                When(is_cancelled=True, then=Value("Отменен")),
                default=F("result__status"),
                output_field=CharField(),
            )
        )
        .values("display_status")
        .annotate(
            results_count=Count("result"),
            average_score=Round(Avg("result__taste_score"), 2),
        )
        .order_by("-results_count", "display_status")
    )
    return overall, by_recipe, by_status
