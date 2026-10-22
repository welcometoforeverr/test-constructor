"""Ensure a usable SQLite file exists after a fresh clone."""
from db.database import DB_PATH, get_connection
from db.import_json import rebuild_database


def ensure_database() -> None:
    """Build the SQLite database from JSON when it is absent or empty."""
    needs_rebuild = not DB_PATH.exists()
    if not needs_rebuild:
        try:
            with get_connection() as connection:
                tables = connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM sqlite_master
                    WHERE type = 'table'
                      AND name IN (
                          'users',
                          'recipes',
                          'experiments',
                          'experiment_results'
                      )
                    """
                ).fetchone()[0]
            needs_rebuild = tables != 4
        except Exception:
            needs_rebuild = True
    if needs_rebuild:
        rebuild_database()
