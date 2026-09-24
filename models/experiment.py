"""Culinary experiment model."""

from .recipe import Recipe
from .result import ExperimentResult
from .user import User


class Experiment:
    """One attempt to change a recipe and record the outcome."""

    def __init__(
        self,
        experiment_id: int,
        user: User,
        recipe: Recipe,
        change: str,
        temperature: int,
        duration_minutes: int,
        experiment_date: str,
        result: ExperimentResult,
        is_cancelled: bool = False,
    ) -> None:
        if temperature <= 0 or duration_minutes <= 0:
            raise ValueError(
                "Температура и время должны быть положительными"
            )
        if not change.strip():
            raise ValueError("Описание изменения не может быть пустым")
        self.id = experiment_id
        self.user = user
        self.recipe = recipe
        self.change = change.strip()
        self.temperature = temperature
        self.duration_minutes = duration_minutes
        self.date = experiment_date
        self.result = result
        self.is_cancelled = is_cancelled

    @property
    def status(self) -> str:
        """Return current experiment state."""
        return "Отменен" if self.is_cancelled else self.result.status

    def cancel(self) -> None:
        """Mark experiment as cancelled without deleting it."""
        self.is_cancelled = True

    def to_data(self) -> dict:
        """Convert object to JSON-compatible data."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "recipe_id": self.recipe.id,
            "change": self.change,
            "temperature": self.temperature,
            "duration_minutes": self.duration_minutes,
            "date": self.date,
            "result": self.result.to_data(),
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        users: dict[int, User],
        recipes: dict[int, Recipe],
    ) -> "Experiment":
        """Restore linked objects from JSON-compatible data."""
        return cls(
            data["id"],
            users[data["user_id"]],
            recipes[data["recipe_id"]],
            data["change"],
            data["temperature"],
            data["duration_minutes"],
            data["date"],
            ExperimentResult.from_data(data["result"]),
            data.get("is_cancelled", False),
        )

    def __str__(self) -> str:
        return (
            f"{self.recipe.name}: {self.change}; {self.status}; "
            f"{self.user.name}"
        )
