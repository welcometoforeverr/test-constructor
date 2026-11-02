"""Persistence tests for console and Django sharing the same SQLite file."""

import pytest
from db.repository import (
    cancel_saved_experiment,
    load_catalog,
    save_experiment,
    save_recipe,
    save_user,
)
from web_experiments.models import Experiment
from web_recipes.models import Recipe
from experiments import create_experiment
from recipes import add_recipe


@pytest.mark.usefixtures("legacy_seed")
def test_console_changes_visible_in_web_queries() -> None:
    """Both components must read and write the same database."""
    users, recipes, experiments = load_catalog()
    save_user(users[0])
    save_user(users[0])
    recipe = add_recipe(recipes, "Борщ", "Супы")
    save_recipe(recipe)
    created = create_experiment(
        experiments,
        users[0],
        recipe,
        "Новая специя",
        95,
        40,
        9,
        "2026-10-22",
    )
    save_experiment(created)

    assert Recipe.objects.get(name="Борщ").id == recipe.id
    assert Experiment.objects.get(pk=created.id).result.taste_score == 9

    new_users, new_recipes, new_experiments = load_catalog()
    assert new_users[0].id == users[0].id
    assert new_recipes[-1].name == "Борщ"
    assert new_experiments[-1].recipe.name == "Борщ"

    assert cancel_saved_experiment(created.id)
    assert load_catalog()[2][-1].is_cancelled
