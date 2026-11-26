"""ORM entities, reusable querysets and localized names."""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class User(models.Model):
    """Domain participant, not a Django authentication account."""

    name = models.CharField("Имя", max_length=200)
    email = models.EmailField("Электронная почта", unique=True)

    class Meta:
        db_table = "users"
        ordering = ["id"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self):
        return self.name


class ExperimentQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(is_cancelled=True)

    def cancelled(self):
        return self.filter(is_cancelled=True)

    def completed(self):
        return self.active().filter(result__isnull=False)

    def for_date(self, day):
        return self.filter(experiment_date=day)

    def with_details(self):
        return self.select_related("recipe", "user", "result")


class Experiment(models.Model):
    objects = ExperimentQuerySet.as_manager()
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="experiments",
        verbose_name="Участник",
    )
    recipe = models.ForeignKey(
        "web_recipes.Recipe", on_delete=models.PROTECT, related_name="experiments",
        verbose_name="Рецепт",
    )
    change_description = models.TextField("Описание изменения")
    temperature = models.PositiveIntegerField(
        "Температура, °C", validators=[MinValueValidator(1)]
    )
    duration_minutes = models.PositiveIntegerField(
        "Время, мин", validators=[MinValueValidator(1)]
    )
    experiment_date = models.DateField("Дата эксперимента", default=timezone.localdate)
    is_cancelled = models.BooleanField("Отменён", default=False)

    class Meta:
        db_table = "experiments"
        ordering = ["-experiment_date", "-id"]
        verbose_name = "Эксперимент"
        verbose_name_plural = "Эксперименты"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(temperature__gt=0), name="positive_temperature"
            ),
            models.CheckConstraint(
                condition=models.Q(duration_minutes__gt=0), name="positive_duration"
            ),
        ]

    @property
    def status(self):
        if self.is_cancelled:
            return "Отменен"
        return self.result.status if hasattr(self, "result") else "Нет результата"

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        return f"Эксперимент №{self.pk}"


class ExperimentResult(models.Model):
    class Outcome(models.TextChoices):
        SUCCESS = "Эксперимент успешный", "Успешный"
        AVERAGE = "Результат удовлетворительный", "Удовлетворительный"
        FAILURE = "Эксперимент неудачный", "Неудачный"

    experiment = models.OneToOneField(
        Experiment, on_delete=models.CASCADE, related_name="result",
        verbose_name="Эксперимент",
    )
    taste_score = models.PositiveSmallIntegerField(
        "Оценка вкуса", validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    status = models.CharField("Результат", max_length=100, choices=Outcome.choices)

    class Meta:
        db_table = "experiment_results"
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(taste_score__gte=1, taste_score__lte=10),
                name="taste_score_between_1_and_10",
            )
        ]

    @classmethod
    def outcome_for_score(cls, score):
        if score >= 8:
            return cls.Outcome.SUCCESS
        if score >= 5:
            return cls.Outcome.AVERAGE
        return cls.Outcome.FAILURE

    def __str__(self):
        return f"{self.taste_score}/10"
