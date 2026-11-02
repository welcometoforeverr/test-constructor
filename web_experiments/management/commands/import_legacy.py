"""Read the PR7 snapshot without modifying it and import all four tables."""

import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from web_recipes.models import Recipe
from web_experiments.models import Experiment, ExperimentResult, User


class Command(BaseCommand):
    help = "Перенос базы ПР7 в пустую ORM-базу с сохранением ID и связей"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=Path,
            default=settings.BASE_DIR / "data" / "culinary_lab.sqlite",
        )

    def handle(self, *args, **options):
        source = options["source"].resolve()
        target = Path(settings.DATABASES["default"]["NAME"]).resolve()
        if source == target:
            raise CommandError("Исходная и целевая базы должны различаться")
        if not source.is_file():
            raise CommandError(f"Исходная база не найдена: {source}")
        try:
            with closing(
                sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)
            ) as connection:
                connection.row_factory = sqlite3.Row
                if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise ValueError("Нарушена целостность исходной базы")
                if connection.execute("PRAGMA foreign_key_check").fetchall():
                    raise ValueError("В исходной базе есть нарушенные внешние ключи")
                rows = {
                    table: [
                        dict(row)
                        for row in connection.execute(f"SELECT * FROM {table}")
                    ]
                    for table in (
                        "users",
                        "recipes",
                        "experiments",
                        "experiment_results",
                    )
                }
            counts = self.transfer(rows)
        except (sqlite3.Error, ValueError) as error:
            raise CommandError(str(error)) from error
        self.stdout.write(
            self.style.SUCCESS(f"Перенесено без изменения источника: {counts}")
        )

    @transaction.atomic
    def transfer(self, rows):
        models = [User, Recipe, Experiment, ExperimentResult]
        if any(model.objects.exists() for model in models):
            raise CommandError(
                "Целевая база не пуста. Перенос отменён; данные не изменены"
            )
        try:
            for model in models:
                for row in rows[model._meta.db_table]:
                    item = model(**row)
                    item.full_clean()
                    item.save(force_insert=True)
            counts = {model._meta.db_table: model.objects.count() for model in models}
            expected = {table: len(items) for table, items in rows.items()}
            if counts != expected:
                raise ValueError("Количество записей после переноса не совпало")
            if Experiment.objects.filter(result__isnull=True).exists():
                raise ValueError("Есть эксперименты без результата")
        except Exception as error:
            raise CommandError(f"Перенос полностью отменён: {error}") from error
        return counts
