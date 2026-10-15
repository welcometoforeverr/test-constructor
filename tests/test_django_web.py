"""Basic integration tests for the read-only Django web layer."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "culinary_site.settings")

import django  # noqa: E402
from django.test import Client  # noqa: E402

django.setup()


def test_homepage_and_lists() -> None:
    client = Client()
    for path in ["/", "/recipes/", "/experiments/"]:
        response = client.get(path)
        assert response.status_code == 200


def test_recipe_and_experiment_detail() -> None:
    client = Client()
    assert client.get("/recipes/1/").status_code == 200
    assert client.get("/experiments/1/").status_code == 200


def test_missing_records_return_404() -> None:
    client = Client()
    assert client.get("/recipes/9999/").status_code == 404
    assert client.get("/experiments/9999/").status_code == 404
    assert client.get("/recipes/not-a-number/").status_code == 404
