"""Console persistence through the same Django models as the website."""

import os

import django
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "culinary_site.settings")
if not apps.ready:
    django.setup()

from django.db import transaction  # noqa: E402
from models import Experiment, Recipe, User  # noqa: E402
from web_recipes.models import Recipe as StoredRecipe  # noqa: E402
from web_experiments.models import (  # noqa: E402
    Experiment as StoredExperiment,
    ExperimentResult,
    User as StoredUser,
)


def load_catalog():
    users = [User(row.pk, row.name, row.email) for row in StoredUser.objects.all()]
    recipes = [
        Recipe(row.pk, row.name, row.category)
        for row in StoredRecipe.objects.order_by("id")
    ]
    user_map = {user.id: user for user in users}
    recipe_map = {recipe.id: recipe for recipe in recipes}
    experiments = []
    for row in StoredExperiment.objects.select_related("result").order_by("id"):
        experiments.append(
            Experiment.from_data(
                {
                    "id": row.pk,
                    "user_id": row.user_id,
                    "recipe_id": row.recipe_id,
                    "change": row.change_description,
                    "temperature": row.temperature,
                    "duration_minutes": row.duration_minutes,
                    "date": row.experiment_date.isoformat(),
                    "is_cancelled": row.is_cancelled,
                    "result": {
                        "taste_score": row.result.taste_score,
                        "status": row.result.status,
                    },
                },
                user_map,
                recipe_map,
            )
        )
    return users, recipes, experiments


def save_user(user):
    try:
        item = StoredUser.objects.get(pk=user.id)
    except StoredUser.DoesNotExist:
        item = StoredUser(pk=user.id)
    item.name, item.email = user.name, user.email
    item.full_clean()
    item.save()


def save_recipe(recipe):
    item = StoredRecipe(pk=recipe.id, name=recipe.name, category=recipe.category)
    item.full_clean()
    item.save(force_insert=True)


@transaction.atomic
def save_experiment(experiment):
    item = StoredExperiment(
        pk=experiment.id,
        user_id=experiment.user.id,
        recipe_id=experiment.recipe.id,
        change_description=experiment.change,
        temperature=experiment.temperature,
        duration_minutes=experiment.duration_minutes,
        experiment_date=experiment.date,
        is_cancelled=experiment.is_cancelled,
    )
    item.full_clean()
    item.save(force_insert=True)
    result = ExperimentResult(
        experiment=item,
        taste_score=experiment.result.taste_score,
        status=experiment.result.status,
    )
    result.full_clean()
    result.save(force_insert=True)


def cancel_saved_experiment(experiment_id):
    return (
        StoredExperiment.objects.filter(pk=experiment_id).update(is_cancelled=True) > 0
    )


def delete_saved_experiment(experiment_id):
    """Delete an experiment and cascade to its result; retain recipe and user."""
    deleted, _ = StoredExperiment.objects.filter(pk=experiment_id).delete()
    return deleted > 0
