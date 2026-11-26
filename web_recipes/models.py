"""Recipe entity managed by Django migrations."""

from uuid import uuid4

from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


def recipe_slug():
    return f"recipe-{uuid4().hex[:16]}"


class Recipe(models.Model):
    name = models.CharField(
        "Название", max_length=200, validators=[MinLengthValidator(3)]
    )
    category = models.CharField("Категория", max_length=100)
    image = models.ImageField("Фото блюда", upload_to="recipes/", blank=True)
    slug = models.SlugField("Адрес", max_length=64, unique=True, default=recipe_slug)

    class Meta:
        db_table = "recipes"
        ordering = ["name", "id"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def get_absolute_url(self):
        return reverse("recipes:slug_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} ({self.category})"
