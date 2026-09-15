from main import (
    build_question_preview,
    get_test_status,
    validate_question,
    validate_test_title,
)


def test_validate_test_title() -> None:
    assert validate_test_title("Основы Python") is True
    assert validate_test_title("  ") is False


def test_validate_question() -> None:
    assert validate_question("Что такое Python?", "A") is True
    assert validate_question("Что?", "E") is False


def test_get_test_status() -> None:
    assert get_test_status(False, True, True) == "Тест готов к публикации"
    assert get_test_status(True, True, True) == "Тест опубликован"


def test_build_question_preview() -> None:
    preview = build_question_preview(
        "Какой тип хранит целые числа?",
        "int",
        "float",
        "str",
        "bool",
        "A",
    )
    assert "A. int" in preview
    assert "Правильный вариант: A" in preview
