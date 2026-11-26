"""PR11 integration tests for forms, CSRF, updates and media."""

from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils import timezone
from PIL import Image

from web_experiments.models import Experiment
from web_recipes.models import Recipe

pytestmark = pytest.mark.django_db


def experiment_data(**changes):
    return {
        "user": 1,
        "recipe": 1,
        "change_description": "Новый способ приготовления",
        "temperature": 170,
        "duration_minutes": 25,
        "experiment_date": timezone.localdate().isoformat(),
        "taste_score": 8,
        **changes,
    }


def test_experiment_create_edit_cancel(legacy_seed, client):
    assert client.get("/experiments/create/").status_code == 200
    response = client.post("/experiments/create/", experiment_data())
    assert response.status_code == 302
    item = Experiment.objects.latest("id")
    assert item.result.taste_score == 8
    assert item.result.status == "Эксперимент успешный"
    url = f"/experiments/{item.pk}/edit/"
    assert client.get(url).context["form"].fields["taste_score"].initial == 8
    assert client.post(url, experiment_data(taste_score=4)).status_code == 302
    item.refresh_from_db()
    assert item.result.taste_score == 4
    assert item.result.status == "Эксперимент неудачный"
    cancel_url = f"/experiments/{item.pk}/cancel/"
    assert client.get(cancel_url).status_code == 405
    assert Client(enforce_csrf_checks=True).post(cancel_url).status_code == 403
    assert client.post(cancel_url).status_code == 302
    item.refresh_from_db()
    assert item.is_cancelled
    assert client.post(url, experiment_data()).status_code == 200
    assert client.get("/experiments/999999/edit/").status_code == 404


@pytest.mark.parametrize("changes", [
    {"taste_score": 11},
    {"temperature": 0},
    {"duration_minutes": 0},
    {"experiment_date": "2999-01-01"},
    {"recipe": 999999},
    {"change_description": "   "},
])
def test_invalid_form_not_saved(legacy_seed, client, changes):
    count = Experiment.objects.count()
    response = client.post("/experiments/create/", experiment_data(**changes))
    assert response.status_code == 200
    assert response.context["form"].errors
    assert Experiment.objects.count() == count


def test_recipe_image_create_and_edit(legacy_seed, client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    buffer = BytesIO()
    Image.new("RGB", (24, 24)).save(buffer, format="PNG")
    upload = SimpleUploadedFile("dish.png", buffer.getvalue(), "image/png")
    response = client.post("/recipes/create/", {
        "name": "Салат", "category": "Закуски", "image": upload,
    })
    assert response.status_code == 302
    item = Recipe.objects.get(name="Салат")
    assert item.image.storage.exists(item.image.name)
    assert item.image.url in client.get(item.get_absolute_url()).content.decode()
    response = client.post(f"/recipes/{item.pk}/edit/", {
        "name": "Новый салат", "category": "Закуски",
    })
    assert response.status_code == 302
    item.refresh_from_db()
    assert item.name == "Новый салат" and item.image
    invalid = SimpleUploadedFile("fake.png", b"not an image", "image/png")
    response = client.post("/recipes/create/", {
        "name": "Плохое фото", "category": "Закуски", "image": invalid,
    })
    assert response.status_code == 200
    assert "image" in response.context["form"].errors
    assert not Recipe.objects.filter(name="Плохое фото").exists()
