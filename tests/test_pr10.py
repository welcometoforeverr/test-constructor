"""PR10: admin configuration, related query performance and slug routing."""

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse

from web_experiments.models import Experiment, ExperimentResult, User
from web_recipes.models import Recipe

pytestmark = pytest.mark.django_db


def test_admin_and_related_inlines(legacy_seed, client):
    for model in (Recipe, User, Experiment, ExperimentResult):
        assert admin.site.is_registered(model)
    account = get_user_model().objects.create_superuser(
        username="test-admin", password="test-password"
    )
    client.force_login(account)
    assert client.get(reverse("admin:index")).status_code == 200
    for model in (Recipe, User, Experiment, ExperimentResult):
        name = f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
        assert client.get(reverse(name)).status_code == 200
    for name in ("admin:web_recipes_recipe_change", "admin:web_experiments_user_change"):
        assert client.get(reverse(name, args=[1])).status_code == 200


def test_slug_and_queryset(legacy_seed, client, django_assert_num_queries):
    recipe = Recipe.objects.get(pk=1)
    assert client.get(recipe.get_absolute_url()).status_code == 200
    assert client.get("/recipes/by-slug/missing/").status_code == 404
    with django_assert_num_queries(1):
        items = list(Experiment.objects.completed().with_details())
        assert items[0].recipe.name and items[0].user.name
        assert items[0].result.taste_score == 9
    items[0].cancel()
    assert Experiment.objects.cancelled().count() == 1
    assert not Experiment.objects.completed().exists()
