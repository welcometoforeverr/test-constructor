"""Preserve existing recipes and assign stable unique slugs."""

import django.core.validators
from django.db import migrations, models

import web_recipes.models


def fill_slugs(apps, schema_editor):
    Recipe = apps.get_model("web_recipes", "Recipe")
    for recipe in Recipe.objects.using(schema_editor.connection.alias).all():
        recipe.slug = f"recipe-{recipe.pk}"
        recipe.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("web_recipes", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ["name", "id"],
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(
                "Название", max_length=200,
                validators=[django.core.validators.MinLengthValidator(3)],
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="category",
            field=models.CharField("Категория", max_length=100),
        ),
        migrations.AddField(
            model_name="recipe",
            name="slug",
            field=models.SlugField("Адрес", max_length=64, null=True),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="recipe",
            name="slug",
            field=models.SlugField(
                "Адрес", max_length=64, unique=True,
                default=web_recipes.models.recipe_slug,
            ),
        ),
    ]
