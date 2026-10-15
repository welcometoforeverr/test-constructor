"""Shared bridge between the OOP/JSON domain and Django web views."""
from pathlib import Path

from models import Experiment, Recipe, User
from storage import load_experiments, load_recipes, load_users

DATA_DIR = Path(__file__).resolve().parent / "data"


def get_recipes() -> list[Recipe]:
    """Load recipe objects from existing JSON storage."""
    return load_recipes(str(DATA_DIR / "recipes.json"))


def get_catalog() -> tuple[list[User], list[Recipe], list[Experiment]]:
    """Load objects and restore links between experiments and owners."""
    users = load_users(str(DATA_DIR / "users.json"))
    recipes = get_recipes()
    experiments = load_experiments(
        str(DATA_DIR / "experiments.json"), users, recipes
    )
    return users, recipes, experiments
