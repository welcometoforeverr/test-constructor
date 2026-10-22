"""Connection helpers for the SQLite layer shared by console and Django."""
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "culinary_lab.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_database_path() -> Path:
    """Resolve an optional test database without changing production data."""
    return Path(os.environ.get("CULINARY_DB_PATH", str(DB_PATH)))


def get_connection(
    database_path: str | Path | None = None,
) -> sqlite3.Connection:
    """Open SQLite with FK constraints enabled and named row access."""
    path = Path(database_path) if database_path is not None else get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=15)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def create_schema(
    database_path: str | Path | None = None,
) -> None:
    """Create project tables, leaving existing content untouched."""
    from contextlib import closing

    with closing(get_connection(database_path)) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.commit()
