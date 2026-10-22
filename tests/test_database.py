"""SQLite schema, JSON import and query tests for PR7."""
import sqlite3

from db.database import DB_PATH, get_connection
from db.import_json import rebuild_database
from db.queries import (
    dashboard_stats,
    experiment_detail,
    experiment_statistics,
    list_experiments,
    list_recipes,
    recipe_categories,
    recipe_detail,
)


def test_import_json_builds_relational_database(tmp_path) -> None:
    database = tmp_path / "culinary_test.sqlite"
    rebuild_database(database)
    with get_connection(database) as connection:
        counts = {
            "users": connection.execute(
                "SELECT COUNT(*) FROM users"
            ).fetchone()[0],
            "recipes": connection.execute(
                "SELECT COUNT(*) FROM recipes"
            ).fetchone()[0],
            "experiments": connection.execute(
                "SELECT COUNT(*) FROM experiments"
            ).fetchone()[0],
            "results": connection.execute(
                "SELECT COUNT(*) FROM experiment_results"
            ).fetchone()[0],
        }
    assert counts == {
        "users": 1,
        "recipes": 2,
        "experiments": 1,
        "results": 1,
    }


def test_database_file_and_tables_exist() -> None:
    assert DB_PATH.exists()
    with get_connection() as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
    assert {
        "users",
        "recipes",
        "experiments",
        "experiment_results",
    }.issubset(tables)


def test_foreign_keys_and_named_rows() -> None:
    with get_connection() as connection:
        foreign_keys = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]
        row = connection.execute(
            "SELECT id, name FROM recipes ORDER BY id LIMIT 1"
        ).fetchone()
    assert foreign_keys == 1
    assert isinstance(row, sqlite3.Row)
    assert row["name"] == "Шоколадный кекс"


def test_sql_query_layer() -> None:
    assert list_recipes("кекс")[0]["id"] == 1
    assert recipe_detail(1)["experiments_count"] >= 1
    assert recipe_categories()
    assert list_experiments(8)[0]["taste_score"] >= 8
    assert experiment_detail(1)["recipe_name"] == "Шоколадный кекс"
    assert dashboard_stats()["recipes_count"] >= 2
    overall, by_recipe, by_status = experiment_statistics()
    assert overall["results_count"] >= 1
    assert by_recipe
    assert by_status
