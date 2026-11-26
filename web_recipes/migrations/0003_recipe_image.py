"""Add an optional photo without changing existing recipes."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("web_recipes", "0002_recipe_admin_slug")]

    operations = [
        migrations.AddField(
            model_name="recipe", name="image",
            field=models.ImageField("Фото блюда", upload_to="recipes/", blank=True),
        ),
    ]
