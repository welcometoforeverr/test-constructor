"""Recipe entity managed by Django migrations."""

from django.core.validators import MinLengthValidator
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    category = models.CharField(max_length=100)

    class Meta:
        db_table = "recipes"
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.name} ({self.category})"
