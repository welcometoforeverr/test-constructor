"""User model."""


class User:
    """Application user who performs culinary experiments."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name.strip()
        self.email = email.strip()

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Create a user object from JSON-compatible data."""
        return cls(data["id"], data["name"], data["email"])

    def to_data(self) -> dict:
        """Convert the object to JSON-compatible data."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
