"""Import the existing PR1-PR6 JSON data into SQLite."""
import json
from pathlib import Path

from db.database import BASE_DIR, create_schema, get_connection

USERS_FILE = BASE_DIR / "data" / "users.json"
RECIPES_FILE = BASE_DIR / "data" / "recipes.json"
EXPERIMENTS_FILE = BASE_DIR / "data" / "experiments.json"


def load_json(filename: Path) -> list[dict]:
    """Load a JSON list from disk."""
    with filename.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в {filename}")
    return data


def import_users(connection) -> None:
    """Transfer users from JSON using executemany()."""
    users = load_json(USERS_FILE)
    connection.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [
            (item["id"], item["name"], item["email"])
            for item in users
        ],
    )


def import_recipes(connection) -> None:
    """Transfer recipes from JSON using executemany()."""
    recipes = load_json(RECIPES_FILE)
    connection.executemany(
        """
        INSERT INTO recipes (id, name, category)
        VALUES (?, ?, ?)
        """,
        [
            (item["id"], item["name"], item["category"])
            for item in recipes
        ],
    )


def import_experiments(connection) -> None:
    """Transfer experiments and nested results from JSON."""
    experiments = load_json(EXPERIMENTS_FILE)
    connection.executemany(
        """
        INSERT INTO experiments (
            id,
            user_id,
            recipe_id,
            change_description,
            temperature,
            duration_minutes,
            experiment_date,
            is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["user_id"],
                item["recipe_id"],
                item["change"],
                item["temperature"],
                item["duration_minutes"],
                item["date"],
                int(item["is_cancelled"]),
            )
            for item in experiments
        ],
    )
    connection.executemany(
        """
        INSERT INTO experiment_results (
            id,
            experiment_id,
            taste_score,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["id"],
                item["result"]["taste_score"],
                item["result"]["status"],
            )
            for item in experiments
        ],
    )


def rebuild_database(database_path=None) -> None:
    """Create schema, clear tables and import the current JSON snapshot."""
    create_schema(database_path)
    connection = get_connection(database_path)
    try:
        connection.execute("DELETE FROM experiment_results")
        connection.execute("DELETE FROM experiments")
        connection.execute("DELETE FROM recipes")
        connection.execute("DELETE FROM users")
        import_users(connection)
        import_recipes(connection)
        import_experiments(connection)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    """Rebuild the default project SQLite database."""
    rebuild_database()


if __name__ == "__main__":
    main()
