"""Live checks for Django pages and console-to-site SQLite synchronization."""
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def assert_http(base: str, path: str, status: int, phrase: str = "") -> None:
    """Verify HTTP status and text against the running Django server."""
    url = base + quote(path, safe="/?=&%")
    try:
        with urlopen(url, timeout=3) as response:
            actual = response.status
            body = response.read().decode("utf-8", "replace")
    except HTTPError as error:
        actual = error.code
        body = error.read().decode("utf-8", "replace")
    assert actual == status, (path, actual, status)
    if phrase:
        assert phrase in body, (path, phrase)
    print(f"HTTP {actual}: {path}", flush=True)


def console_smoke(db_path: Path) -> None:
    """Create a recipe and an experiment in a disposable SQLite database."""
    env = {**os.environ, "CULINARY_DB_PATH": str(db_path)}
    choices = (
        "1\n"
        "3\n"
        "Борщ\n"
        "Супы\n"
        "4\n"
        "3\n"
        "Добавил специи\n"
        "90\n"
        "25\n"
        "8\n"
        "7\n"
        "0\n"
    )
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=choices,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=env,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Борщ" in result.stdout
    assert "Эксперимент успешный" in result.stdout

    with sqlite3.connect(db_path) as connection:
        recipe = connection.execute(
            "SELECT id FROM recipes WHERE name = 'Борщ'"
        ).fetchone()
        assert recipe is not None
        experiment = connection.execute(
            "SELECT id FROM experiments WHERE recipe_id = ?",
            (recipe[0],),
        ).fetchone()
        assert experiment is not None
    print("PASS: console stores recipe and experiment in SQLite", flush=True)


def http_smoke() -> None:
    """Run real Django server and verify immediate console data visibility."""
    with tempfile.TemporaryDirectory() as name:
        sandbox = Path(name)
        db_path = sandbox / "culinary_lab.sqlite"
        shutil.copyfile(ROOT / "data" / "culinary_lab.sqlite", db_path)
        env = {**os.environ, "CULINARY_DB_PATH": str(db_path)}
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        base = f"http://127.0.0.1:{port}"
        server = subprocess.Popen(
            [
                sys.executable, "manage.py", "runserver",
                f"127.0.0.1:{port}", "--noreload",
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        try:
            for _ in range(50):
                if server.poll() is not None:
                    raise AssertionError("Django server terminated")
                try:
                    with urlopen(base + "/", timeout=1) as response:
                        assert response.status == 200
                    break
                except (URLError, TimeoutError):
                    time.sleep(0.2)
            else:
                raise AssertionError("Django server did not start")

            routes = [
                ("/", 200, "новый эксперимент"),
                ("/recipes/", 200, "Шоколадный кекс"),
                ("/recipes/1/", 200, "Шоколадный кекс"),
                ("/recipes/categories/", 200, "Рецепты по категориям"),
                ("/experiments/", 200, "Эксперименты"),
                ("/experiments/1/", 200, "Калугин Никита"),
                ("/experiments/statistics/", 200, "Статистика"),
                ("/recipes/?q=кекс", 200, "Шоколадный кекс"),
                ("/recipes/?q=небывает", 200, "ничего не найдено"),
                ("/experiments/?min_score=8", 200, "Шоколадный кекс"),
                ("/experiments/?min_score=abc", 200, "Шоколадный кекс"),
                ("/recipes/9999/", 404, "не найден"),
                ("/experiments/9999/", 404, "не найден"),
                ("/static/homepage/css/style.css", 200, "--accent"),
                ("/static/homepage/js/main.js", 200, "contrast-toggle"),
                ("/static/homepage/img/logo.svg", 200, "<svg"),
            ]
            for path, code, marker in routes:
                assert_http(base, path, code, marker)

            console_smoke(db_path)
            assert_http(base, "/recipes/?q=Борщ", 200, "Борщ")
            assert_http(base, "/recipes/3/", 200, "Борщ")
            assert_http(base, "/experiments/", 200, "Добавил специи")
            print("PASS: console updates are visible on running site", flush=True)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
    print("PASS: complete live smoke suite", flush=True)


if __name__ == "__main__":
    http_smoke()
