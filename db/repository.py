"""Shared domain persistence: the console writes to the Django SQLite DB."""
from contextlib import closing

from db.bootstrap import ensure_database
from db.database import get_connection
from models import Experiment, Recipe, User


def load_catalog() -> tuple[list[User], list[Recipe], list[Experiment]]:
    """Load OOP objects from the same SQLite database Django reads."""
    ensure_database()
    with closing(get_connection()) as connection:
        users = [
            User(row["id"], row["name"], row["email"])
            for row in connection.execute(
                "SELECT id, name, email FROM users ORDER BY id"
            )
        ]
        recipes = [
            Recipe(row["id"], row["name"], row["category"])
            for row in connection.execute(
                "SELECT id, name, category FROM recipes ORDER BY id"
            )
        ]
        user_map = {user.id: user for user in users}
        recipe_map = {recipe.id: recipe for recipe in recipes}
        experiments = []
        rows = connection.execute(
            """
            SELECT e.*, r.taste_score, r.status
            FROM experiments AS e
            JOIN experiment_results AS r ON r.experiment_id = e.id
            ORDER BY e.id
            """
        ).fetchall()
        for row in rows:
            data = {
                "id": row["id"],
                "user_id": row["user_id"],
                "recipe_id": row["recipe_id"],
                "change": row["change_description"],
                "temperature": row["temperature"],
                "duration_minutes": row["duration_minutes"],
                "date": row["experiment_date"],
                "result": {
                    "taste_score": row["taste_score"],
                    "status": row["status"],
                },
                "is_cancelled": bool(row["is_cancelled"]),
            }
            experiments.append(
                Experiment.from_data(data, user_map, recipe_map)
            )
    return users, recipes, experiments


def save_user(user: User) -> None:
    """Store a user (including the default console user)."""
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO users (id, name, email)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name, email = excluded.email
                """,
                (user.id, user.name, user.email),
            )


def save_recipe(recipe: Recipe) -> None:
    """Persist a newly created recipe immediately."""
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                "INSERT INTO recipes (id, name, category) VALUES (?, ?, ?)",
                (recipe.id, recipe.name, recipe.category),
            )


def save_experiment(experiment: Experiment) -> None:
    """Atomically insert an experiment and its separate result record."""
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO experiments (
                    id, user_id, recipe_id, change_description,
                    temperature, duration_minutes, experiment_date,
                    is_cancelled
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    experiment.id,
                    experiment.user.id,
                    experiment.recipe.id,
                    experiment.change,
                    experiment.temperature,
                    experiment.duration_minutes,
                    experiment.date,
                    int(experiment.is_cancelled),
                ),
            )
            connection.execute(
                """
                INSERT INTO experiment_results (
                    id, experiment_id, taste_score, status
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    experiment.id,
                    experiment.id,
                    experiment.result.taste_score,
                    experiment.result.status,
                ),
            )


def cancel_saved_experiment(experiment_id: int) -> bool:
    """Mark an existing experiment as cancelled without deleting history."""
    with closing(get_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "UPDATE experiments SET is_cancelled = 1 WHERE id = ?",
                (experiment_id,),
            )
            return cursor.rowcount > 0
