"""Initialize the SQLite database only when necessary."""
from db.database import get_connection, get_database_path
from db.import_json import rebuild_database


def ensure_database() -> None:
    """Migrate initial JSON only if the database is absent or uninitialized."""
    from contextlib import closing

    path = get_database_path()
    needs_rebuild = not path.exists()
    if not needs_rebuild:
        try:
            with closing(get_connection(path)) as connection:
                tables = connection.execute(
                    """
                    SELECT COUNT(*) FROM sqlite_master
                    WHERE type = 'table'
                      AND name IN (
                          'users', 'recipes', 'experiments',
                          'experiment_results'
                      )
                    """
                ).fetchone()[0]
            needs_rebuild = tables != 4
        except Exception:
            needs_rebuild = True
    if needs_rebuild:
        rebuild_database(path)
