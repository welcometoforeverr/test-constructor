"""Named, parameterized SQL operations used by Django views."""
from db.bootstrap import ensure_database
from db.database import get_connection

ensure_database()


def fetch_all(query: str, params: tuple = ()) -> list:
    """Execute SELECT and return sqlite3.Row objects."""
    with get_connection() as connection:
        return connection.execute(query, params).fetchall()


def fetch_one(query: str, params: tuple = ()):
    """Execute SELECT and return one sqlite3.Row or None."""
    with get_connection() as connection:
        return connection.execute(query, params).fetchone()


def list_recipes(search: str = "", category: str = "") -> list:
    """Return recipes with optional parameterized filters."""
    query = """
        SELECT
            recipes.id,
            recipes.name,
            recipes.category,
            COUNT(e.id) AS experiments_count
        FROM recipes
        LEFT JOIN experiments AS e ON e.recipe_id = recipes.id
        WHERE recipes.name LIKE ?
          AND recipes.category LIKE ?
        GROUP BY recipes.id, recipes.name, recipes.category
        ORDER BY recipes.name
    """
    return fetch_all(query, (f"%{search}%", f"%{category}%"))


def recipe_detail(recipe_id: int):
    """Return one recipe with aggregate experiment statistics."""
    return fetch_one(
        """
        SELECT
            recipes.id,
            recipes.name,
            recipes.category,
            COUNT(e.id) AS experiments_count,
            ROUND(AVG(r.taste_score), 2) AS average_score
        FROM recipes
        LEFT JOIN experiments AS e ON e.recipe_id = recipes.id
        LEFT JOIN experiment_results AS r ON r.experiment_id = e.id
        WHERE recipes.id = ?
        GROUP BY recipes.id, recipes.name, recipes.category
        """,
        (recipe_id,),
    )


def recipe_categories() -> list:
    """Return recipe counts grouped by category."""
    return fetch_all(
        """
        SELECT category, COUNT(*) AS recipes_count
        FROM recipes
        GROUP BY category
        ORDER BY recipes_count DESC, category
        """
    )


def list_experiments(min_score: int = 1) -> list:
    """Return joined experiment rows filtered by taste score."""
    return fetch_all(
        """
        SELECT
            e.id,
            e.experiment_date,
            e.change_description,
            e.temperature,
            e.duration_minutes,
            e.is_cancelled,
            recipes.id AS recipe_id,
            recipes.name AS recipe_name,
            users.name AS user_name,
            r.taste_score,
            r.status
        FROM experiments AS e
        JOIN recipes ON recipes.id = e.recipe_id
        JOIN users ON users.id = e.user_id
        JOIN experiment_results AS r ON r.experiment_id = e.id
        WHERE r.taste_score >= ?
        ORDER BY e.experiment_date DESC, e.id DESC
        """,
        (min_score,),
    )


def experiment_detail(experiment_id: int):
    """Return one joined experiment row."""
    return fetch_one(
        """
        SELECT
            e.id,
            e.experiment_date,
            e.change_description,
            e.temperature,
            e.duration_minutes,
            e.is_cancelled,
            recipes.id AS recipe_id,
            recipes.name AS recipe_name,
            recipes.category AS recipe_category,
            users.name AS user_name,
            users.email AS user_email,
            r.taste_score,
            r.status
        FROM experiments AS e
        JOIN recipes ON recipes.id = e.recipe_id
        JOIN users ON users.id = e.user_id
        JOIN experiment_results AS r ON r.experiment_id = e.id
        WHERE e.id = ?
        """,
        (experiment_id,),
    )


def dashboard_stats() -> dict:
    """Return aggregate counters for the home page."""
    counts = fetch_one(
        """
        SELECT
            (SELECT COUNT(*) FROM users) AS users_count,
            (SELECT COUNT(*) FROM recipes) AS recipes_count,
            (SELECT COUNT(*) FROM experiments) AS experiments_count,
            (SELECT ROUND(AVG(taste_score), 2)
             FROM experiment_results) AS average_score
        """
    )
    return dict(counts) if counts else {}


def experiment_statistics() -> tuple[dict, list, list]:
    """Return overall, per-recipe and per-status statistics."""
    overall = fetch_one(
        """
        SELECT
            COUNT(*) AS results_count,
            ROUND(AVG(taste_score), 2) AS average_score,
            MIN(taste_score) AS min_score,
            MAX(taste_score) AS max_score
        FROM experiment_results
        """
    )
    by_recipe = fetch_all(
        """
        SELECT
            recipes.name AS recipe_name,
            COUNT(e.id) AS experiments_count,
            ROUND(AVG(r.taste_score), 2) AS average_score
        FROM recipes
        LEFT JOIN experiments AS e ON e.recipe_id = recipes.id
        LEFT JOIN experiment_results AS r ON r.experiment_id = e.id
        GROUP BY recipes.id, recipes.name
        ORDER BY experiments_count DESC, recipes.name
        """
    )
    by_status = fetch_all(
        """
        SELECT
            status,
            COUNT(*) AS results_count,
            ROUND(AVG(taste_score), 2) AS average_score
        FROM experiment_results
        GROUP BY status
        ORDER BY results_count DESC, status
        """
    )
    return dict(overall) if overall else {}, by_recipe, by_status
