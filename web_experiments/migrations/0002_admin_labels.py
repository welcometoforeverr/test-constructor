"""Localize fields and preserve existing stored result text."""

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web_experiments", "0001_initial"),
        ("web_recipes", "0002_recipe_admin_slug"),
    ]
    operations = [
        migrations.AlterModelOptions(
            name="user", options={
                "ordering": ["id"], "verbose_name": "Участник",
                "verbose_name_plural": "Участники",
            },
        ),
        migrations.AlterModelOptions(
            name="experiment", options={
                "ordering": ["-experiment_date", "-id"],
                "verbose_name": "Эксперимент", "verbose_name_plural": "Эксперименты",
            },
        ),
        migrations.AlterModelOptions(
            name="experimentresult", options={
                "verbose_name": "Результат", "verbose_name_plural": "Результаты",
            },
        ),
        migrations.AlterField(
            model_name="user", name="name",
            field=models.CharField("Имя", max_length=200),
        ),
        migrations.AlterField(
            model_name="user", name="email",
            field=models.EmailField("Электронная почта", max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="experiment", name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="experiments", to="web_experiments.user",
                verbose_name="Участник",
            ),
        ),
        migrations.AlterField(
            model_name="experiment", name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="experiments", to="web_recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="experiment", name="change_description",
            field=models.TextField("Описание изменения"),
        ),
        migrations.AlterField(
            model_name="experiment", name="temperature",
            field=models.PositiveIntegerField(
                "Температура, °C", validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AlterField(
            model_name="experiment", name="duration_minutes",
            field=models.PositiveIntegerField(
                "Время, мин", validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AlterField(
            model_name="experiment", name="experiment_date",
            field=models.DateField("Дата эксперимента", default=django.utils.timezone.localdate),
        ),
        migrations.AlterField(
            model_name="experiment", name="is_cancelled",
            field=models.BooleanField("Отменён", default=False),
        ),
        migrations.AlterField(
            model_name="experimentresult", name="experiment",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="result", to="web_experiments.experiment",
                verbose_name="Эксперимент",
            ),
        ),
        migrations.AlterField(
            model_name="experimentresult", name="taste_score",
            field=models.PositiveSmallIntegerField(
                "Оценка вкуса", validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="experimentresult", name="status",
            field=models.CharField(
                "Результат", max_length=100, choices=[
                    ("Эксперимент успешный", "Успешный"),
                    ("Результат удовлетворительный", "Удовлетворительный"),
                    ("Эксперимент неудачный", "Неудачный"),
                ],
            ),
        ),
    ]
