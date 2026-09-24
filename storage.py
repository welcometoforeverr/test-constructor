"""JSON storage helpers for the project."""

import json
from pathlib import Path


def load_data(filename: str) -> list[dict]:
    """Load dictionaries from JSON; return an empty list if absent."""
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {filename}") from error

    if not isinstance(data, list):
        raise ValueError(f"Ожидался список в файле {filename}")
    return data


def save_data(filename: str, data: list[dict]) -> None:
    """Save project data to JSON using a context manager."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
