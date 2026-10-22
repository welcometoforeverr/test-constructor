"""Connection helpers for the PR7 SQLite layer."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "culinary_lab.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(
    database_path: str | Path | None = None,
) -> sqlite3.Connection:
    """Return a configured SQLite connection with named rows."""
    path = Path(database_path) if database_path else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def create_schema(
    database_path: str | Path | None = None,
) -> None:
    """Create all project tables from sql/schema.sql."""
    with get_connection(database_path) as connection:
        connection.executescript(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )
        connection.commit()
