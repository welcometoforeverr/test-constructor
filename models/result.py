"""Experiment result model."""


class ExperimentResult:
    """Result of a culinary experiment."""

    def __init__(self, taste_score: int, status: str) -> None:
        if not 1 <= taste_score <= 10:
            raise ValueError("Оценка вкуса должна быть от 1 до 10")
        self.taste_score = taste_score
        self.status = status

    @classmethod
    def from_score(cls, taste_score: int) -> "ExperimentResult":
        """Create result according to the taste score."""
        if taste_score >= 8:
            status = "Эксперимент успешный"
        elif taste_score >= 5:
            status = "Результат удовлетворительный"
        else:
            status = "Эксперимент неудачный"
        return cls(taste_score, status)

    @classmethod
    def from_data(cls, data: dict) -> "ExperimentResult":
        """Create result from JSON-compatible data."""
        return cls(data["taste_score"], data["status"])

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        return {"taste_score": self.taste_score, "status": self.status}

    def __str__(self) -> str:
        return f"{self.status}, оценка {self.taste_score}/10"
