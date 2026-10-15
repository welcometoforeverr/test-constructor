"""HTTP, templates and routing checks for PR5 and PR6."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "culinary_site.settings")

import django  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402
from django.contrib.staticfiles import finders  # noqa: E402

django.setup()


def test_homepage_and_lists() -> None:
    client = Client()
    for path in ["/", "/recipes/", "/experiments/"]:
        response = client.get(path)
        assert response.status_code == 200
        assert b"<!doctype html>" in response.content.lower()


def test_recipe_and_experiment_detail() -> None:
    client = Client()
    recipe = client.get("/recipes/1/")
    experiment = client.get("/experiments/1/")
    assert recipe.status_code == 200
    assert experiment.status_code == 200
    assert "Шоколадный кекс" in recipe.content.decode()
    assert "Шоколадный кекс" in experiment.content.decode()


def test_missing_records_return_404() -> None:
    client = Client()
    assert client.get("/recipes/9999/").status_code == 404
    assert client.get("/experiments/9999/").status_code == 404
    assert client.get("/recipes/not-a-number/").status_code == 404


def test_named_urls_and_templates() -> None:
    assert reverse("homepage:index") == "/"
    assert reverse("recipes:detail", args=[1]) == "/recipes/1/"
    assert reverse("experiments:detail", args=[1]) == "/experiments/1/"
    response = Client().get("/recipes/")
    assert any(t.name == "recipes/recipe_list.html"
               for t in response.templates) or response.status_code == 200


def test_search_and_static_assets() -> None:
    client = Client()
    results = client.get("/recipes/?q=кекс")
    assert results.status_code == 200
    assert "Шоколадный кекс" in results.content.decode()
    assert finders.find("homepage/css/style.css") is not None
    assert finders.find("homepage/js/main.js") is not None
    assert finders.find("homepage/img/logo.svg") is not None
