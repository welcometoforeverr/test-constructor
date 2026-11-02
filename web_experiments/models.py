"""Participants, experiments and their one-to-one results for PR9."""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class User(models.Model):
    """Domain participant; separate from Django authentication users."""

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "users"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Experiment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="experiments")
    recipe = models.ForeignKey(
        "web_recipes.Recipe", on_delete=models.PROTECT, related_name="experiments"
    )
    change_description = models.TextField()
    temperature = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    experiment_date = models.DateField(default=timezone.localdate)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        db_table = "experiments"
        ordering = ["-experiment_date", "-id"]
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
    experiment = models.OneToOneField(
        Experiment, on_delete=models.CASCADE, related_name="result"
    )
    taste_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "experiment_results"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(taste_score__gte=1, taste_score__lte=10),
                name="taste_score_between_1_and_10",
            )
        ]

    def __str__(self):
        return f"{self.taste_score}/10"
