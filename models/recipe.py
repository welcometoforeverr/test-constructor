"""Recipe model."""


class Recipe:
    """Recipe used as a base for culinary experiments."""

    def __init__(self, recipe_id: int, name: str, category: str) -> None:
        if not self.validate_name(name):
            raise ValueError(
                "Название рецепта должно содержать минимум 3 символа"
            )
        if not category.strip():
            raise ValueError("Категория рецепта не может быть пустой")
        self.id = recipe_id
        self.name = name.strip()
        self.category = category.strip()

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate recipe name without using instance state."""
        return len(name.strip()) >= 3

    @classmethod
    def from_data(cls, data: dict) -> "Recipe":
        """Create a recipe object from JSON-compatible data."""
        return cls(data["id"], data["name"], data["category"])

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        return {"id": self.id, "name": self.name, "category": self.category}

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"
