"""Persistence tests for console and Django sharing the same SQLite file."""
from db.import_json import rebuild_database
from db.repository import (
    cancel_saved_experiment,
    load_catalog,
    save_experiment,
    save_recipe,
)
from db.queries import experiment_detail, list_recipes
from experiments import create_experiment
from recipes import add_recipe


def test_console_changes_visible_in_web_queries(tmp_path, monkeypatch) -> None:
    """Both components must read and write the same database."""
    path = tmp_path / "shared.sqlite"
    monkeypatch.setenv("CULINARY_DB_PATH", str(path))
    rebuild_database(path)

    users, recipes, experiments = load_catalog()
    recipe = add_recipe(recipes, "Борщ", "Супы")
    save_recipe(recipe)
    created = create_experiment(
        experiments, users[0], recipe, "Новая специя",
        95, 40, 9, "2026-10-22",
    )
    save_experiment(created)

    assert list_recipes("Борщ")[0]["id"] == recipe.id
    assert experiment_detail(created.id)["taste_score"] == 9

    new_users, new_recipes, new_experiments = load_catalog()
    assert new_users[0].id == users[0].id
    assert new_recipes[-1].name == "Борщ"
    assert new_experiments[-1].recipe.name == "Борщ"

    assert cancel_saved_experiment(created.id)
    assert load_catalog()[2][-1].is_cancelled
