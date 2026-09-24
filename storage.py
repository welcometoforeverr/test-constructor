"""Load and save domain objects in JSON files."""

import json
from pathlib import Path

from models import Experiment, Recipe, User


def _load_json(filename: str) -> list[dict]:
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {filename}") from error
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в файле {filename}")
    return data


def _save_json(filename: str, data: list[dict]) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Load User objects from JSON."""
    return [User.from_data(data) for data in _load_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Save User objects to JSON."""
    _save_json(filename, [user.to_data() for user in users])


def load_recipes(filename: str) -> list[Recipe]:
    """Load Recipe objects from JSON."""
    return [Recipe.from_data(data) for data in _load_json(filename)]


def save_recipes(filename: str, recipes: list[Recipe]) -> None:
    """Save Recipe objects to JSON."""
    _save_json(filename, [recipe.to_data() for recipe in recipes])


def load_experiments(
    filename: str,
    users: list[User],
    recipes: list[Recipe],
) -> list[Experiment]:
    """Load Experiment objects and restore links to User and Recipe."""
    users_by_id = {user.id: user for user in users}
    recipes_by_id = {recipe.id: recipe for recipe in recipes}
    return [
        Experiment.from_data(data, users_by_id, recipes_by_id)
        for data in _load_json(filename)
    ]


def save_experiments(filename: str, experiments: list[Experiment]) -> None:
    """Save Experiment objects to JSON."""
    _save_json(filename, [experiment.to_data() for experiment in experiments])
