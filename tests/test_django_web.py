"""HTTP and routing checks including PR7 SQLite pages."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "culinary_site.settings")

import django  # noqa: E402
from django.contrib.staticfiles import finders  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

django.setup()


def test_main_sqlite_pages() -> None:
    client = Client()
    paths = [
        "/",
        "/recipes/",
        "/recipes/categories/",
        "/experiments/",
        "/experiments/statistics/",
    ]
    for path in paths:
        assert client.get(path).status_code == 200


def test_detail_pages_and_joined_data() -> None:
    client = Client()
    recipe = client.get("/recipes/1/")
    experiment = client.get("/experiments/1/")
    assert recipe.status_code == 200
    assert experiment.status_code == 200
    assert "Шоколадный кекс" in recipe.content.decode()
    assert "Калугин Никита" in experiment.content.decode()


def test_parameterized_filters() -> None:
    client = Client()
    recipes = client.get("/recipes/?q=кекс&category=Выпечка")
    experiments = client.get("/experiments/?min_score=8")
    assert recipes.status_code == 200
    assert "Шоколадный кекс" in recipes.content.decode()
    assert experiments.status_code == 200
    assert "9/10" in experiments.content.decode()


def test_missing_records_return_404() -> None:
    client = Client()
    assert client.get("/recipes/9999/").status_code == 404
    assert client.get("/experiments/9999/").status_code == 404
    assert client.get("/recipes/not-a-number/").status_code == 404


def test_named_urls_and_static_assets() -> None:
    assert reverse("recipes:categories") == "/recipes/categories/"
    assert reverse("experiments:statistics") == "/experiments/statistics/"
    assert reverse("recipes:detail", args=[1]) == "/recipes/1/"
    assert finders.find("homepage/css/style.css") is not None
    assert finders.find("homepage/js/main.js") is not None
    assert finders.find("homepage/img/logo.svg") is not None
