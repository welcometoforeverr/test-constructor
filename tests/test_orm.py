"""PR9 regression tests for transfer, relationships, queries and pagination."""

import hashlib
import shutil
import sqlite3
from datetime import date

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

from db.repository import delete_saved_experiment
from web_experiments.models import Experiment, ExperimentResult, User
from web_experiments.queries import experiment_catalog, experiment_statistics
from web_recipes.models import Recipe
from web_recipes.queries import recipe_catalog

pytestmark = pytest.mark.django_db
SOURCE = settings.BASE_DIR / "data" / "culinary_lab.sqlite"


def create_attempt(recipe, user, score=8, day=2):
    item = Experiment.objects.create(
        recipe=recipe,
        user=user,
        change_description="Меньше сахара",
        temperature=180,
        duration_minutes=30,
        experiment_date=date(2026, 11, day),
    )
    ExperimentResult.objects.create(
        experiment=item, taste_score=score, status="Эксперимент успешный"
    )
    return item


def test_import_preserves_every_value_and_source():
    before = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    call_command("import_legacy")
    with sqlite3.connect(SOURCE) as source:
        source.row_factory = sqlite3.Row
        for model in [User, Recipe, Experiment, ExperimentResult]:
            rows = source.execute(f"SELECT * FROM {model._meta.db_table}").fetchall()
            assert model.objects.count() == len(rows)
            for row in rows:
                actual = model.objects.get(pk=row["id"])
                for key in row.keys():
                    value = getattr(actual, key)
                    if isinstance(value, date):
                        value = value.isoformat()
                    assert value == row[key]
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == before


def test_reimport_refuses_to_overwrite(legacy_seed):
    recipe = Recipe.objects.create(name="Новый рецепт", category="Десерт")
    with pytest.raises(CommandError, match="не пуста"):
        call_command("import_legacy")
    assert Recipe.objects.get(pk=recipe.pk).name == "Новый рецепт"


def test_invalid_source_rolls_back_all_tables(tmp_path):
    source = tmp_path / "invalid.sqlite"
    shutil.copyfile(SOURCE, source)
    with sqlite3.connect(source) as connection:
        connection.execute("UPDATE experiments SET experiment_date = 'wrong'")
    with pytest.raises(CommandError, match="отменён"):
        call_command("import_legacy", source=source)
    for model in [User, Recipe, Experiment, ExperimentResult]:
        assert model.objects.count() == 0


def test_missing_source_does_not_create_file(tmp_path):
    source = tmp_path / "missing.sqlite"
    with pytest.raises(CommandError, match="не найдена"):
        call_command("import_legacy", source=source)
    assert not source.exists()


def test_relationships_protect_and_cascade(legacy_seed):
    item = Experiment.objects.select_related("recipe", "user", "result").get(pk=1)
    assert item.user.experiments.get(pk=1) == item
    assert item.recipe.experiments.get(pk=1) == item
    assert item.result.experiment == item
    with pytest.raises(ProtectedError):
        item.recipe.delete()
    with pytest.raises(ProtectedError):
        item.user.delete()
    assert delete_saved_experiment(item.pk)
    assert not ExperimentResult.objects.exists()
    assert Recipe.objects.count() == 2 and User.objects.count() == 1
    assert not delete_saved_experiment(9999)


def test_cancel_updates_status_and_filters(legacy_seed, client):
    item = Experiment.objects.get(pk=1)
    item.cancel()
    item.refresh_from_db()
    assert item.is_cancelled and item.status == "Отменен"
    assert not experiment_catalog({"status": "active"}).exists()
    assert experiment_catalog({"status": "cancelled"}).get() == item
    assert "Отменен" in client.get("/experiments/1/").content.decode()
    assert experiment_statistics()[2].get()["display_status"] == "Отменен"


def test_validation_and_db_constraints(legacy_seed):
    item = ExperimentResult.objects.get(experiment_id=1)
    item.taste_score = 11
    with pytest.raises(ValidationError):
        item.full_clean()
    with pytest.raises(IntegrityError), transaction.atomic():
        item.save()
    with pytest.raises(IntegrityError), transaction.atomic():
        Experiment.objects.filter(pk=1).update(temperature=0)
    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create(name="Другой", email=User.objects.first().email)


def test_search_filters_sort_and_empty_recipes(legacy_seed):
    recipe = Recipe.objects.create(name="Тестовый суп", category="Супы")
    user = User.objects.get(pk=1)
    first = create_attempt(recipe, user, score=7, day=1)
    second = create_attempt(recipe, user, score=10, day=2)
    filters = {"recipe": recipe, "date": date(2026, 11, 2), "min_score": 8}
    assert list(experiment_catalog(filters)) == [second]
    assert experiment_catalog({"q": "Тестовый"}).count() == 2
    assert experiment_catalog({"q": user.name}).count() == 3
    assert experiment_catalog({"q": "сахара"}).count() >= 2
    assert experiment_catalog({"q": "неттакого"}).count() == 0
    assert list(experiment_catalog({"recipe": recipe, "sort": "oldest"})) == [
        first,
        second,
    ]
    assert list(experiment_catalog({"recipe": recipe, "sort": "score"})) == [
        second,
        first,
    ]
    empty = Recipe.objects.create(name="Без опытов", category="Супы")
    assert recipe_catalog().get(pk=empty.pk).experiments_count == 0
    assert recipe_catalog("Тестовый", "Супы").get().pk == recipe.pk
    assert recipe_catalog().get(pk=recipe.pk).average_score == 8.5
    overall, by_recipe, _ = experiment_statistics()
    assert overall["results_count"] == 3
    assert overall["min_score"] == 7 and overall["max_score"] == 10
    assert by_recipe.get(pk=empty.pk).experiments_count == 0


def test_related_objects_use_one_query(legacy_seed, django_assert_num_queries):
    with django_assert_num_queries(1):
        items = list(experiment_catalog({}))
        assert items[0].recipe.name and items[0].user.name
        assert items[0].result.taste_score == 9


@pytest.mark.parametrize(
    "params",
    [
        {"date": "2026-02-30", "recipe": "abc", "sort": "DROP TABLE recipes"},
        {"min_score": "abc", "page": "abc"},
        {"min_score": "99", "recipe": "999999"},
        {"min_score": "-5", "page": "-1"},
        {"q": "' OR 1=1 --", "page": "99999999999999999"},
    ],
)
def test_invalid_parameters_are_safe(legacy_seed, client, params):
    assert client.get("/experiments/", params).status_code == 200
    assert Recipe.objects.count() == 2


def test_pagination_preserves_all_filters(legacy_seed, client):
    recipe, user = Recipe.objects.get(pk=1), User.objects.get(pk=1)
    for _ in range(11):
        create_attempt(recipe, user)
    params = {
        "recipe": recipe.pk,
        "date": "2026-11-02",
        "status": "active",
        "q": "сахара",
        "min_score": 8,
        "sort": "score",
    }
    response = client.get("/experiments/", params)
    page = response.context["page_obj"]
    assert page.paginator.count == 11
    assert page.paginator.num_pages == 3 and len(page) == 5
    body = response.content.decode()
    assert "page=2" in body
    for key in ["recipe", "date", "status", "q", "min_score", "sort"]:
        assert f"{key}=" in body
    second = client.get("/experiments/", {**params, "page": 2}).context["page_obj"]
    assert not set(item.pk for item in page) & set(item.pk for item in second)
    last = client.get("/experiments/", {**params, "page": 99999}).context["page_obj"]
    assert last.number == 3 and len(last) == 1


def test_empty_database_pages(client):
    for path in [
        "/",
        "/recipes/",
        "/recipes/categories/",
        "/experiments/",
        "/experiments/statistics/",
    ]:
        assert client.get(path).status_code == 200
    assert client.get("/experiments/1/").status_code == 404
