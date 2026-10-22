"""Run complete HTTP and console smoke checks against the current project."""
import json
import shutil
import socket
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
    """Check an actual Django HTTP response and optional body text."""
    try:
        with urlopen(base + quote(path, safe="/?=&%"), timeout=3) as response:
            actual = response.status
            body = response.read().decode("utf-8", "replace")
    except HTTPError as error:
        actual = error.code
        body = error.read().decode("utf-8", "replace")
    assert actual == status, (path, actual, status)
    if phrase:
        assert phrase in body, (path, phrase)
    print(f"HTTP {actual}: {path}", flush=True)


def http_smoke() -> None:
    """Launch actual runserver and exercise real HTTP endpoints."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    base = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [
            sys.executable,
            "manage.py",
            "runserver",
            f"127.0.0.1:{port}",
            "--noreload",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    try:
        for _ in range(50):
            if server.poll() is not None:
                raise AssertionError(
                    f"Django server terminated: {server.returncode}"
                )
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
        for path, expected, marker in routes:
            assert_http(base, path, expected, marker)
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()
    print("PASS: real Django server HTTP smoke", flush=True)


def console_smoke() -> None:
    """Run console interactively with a disposable copy of JSON files."""
    with tempfile.TemporaryDirectory() as name:
        workspace = Path(name)
        (workspace / "data").mkdir()
        for filename in ("users.json", "recipes.json", "experiments.json"):
            shutil.copyfile(ROOT / "data" / filename, workspace / "data" / filename)

        input_text = (
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
            [sys.executable, str(ROOT / "main.py")],
            input=input_text,
            text=True,
            capture_output=True,
            cwd=workspace,
            timeout=15,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert "Борщ" in result.stdout
        assert "Эксперимент успешный" in result.stdout
        recipes = json.loads((workspace / "data/recipes.json").read_text(
            encoding="utf-8"
        ))
        experiments = json.loads((workspace / "data/experiments.json").read_text(
            encoding="utf-8"
        ))
        assert any(recipe["name"] == "Борщ" for recipe in recipes)
        assert any(
            experiment["recipe_id"] == 3
            for experiment in experiments
        )
        print("PASS: console add recipe/experiment and JSON save", flush=True)


if __name__ == "__main__":
    http_smoke()
    console_smoke()
    print("PASS: full smoke suite", flush=True)
