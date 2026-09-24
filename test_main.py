from main import (
    build_experiment_preview,
    get_experiment_result,
    validate_experiment,
    validate_recipe_name,
)


def test_validate_recipe_name() -> None:
    assert validate_recipe_name("Шоколадный кекс") is True
    assert validate_recipe_name("  ") is False


def test_validate_experiment() -> None:
    assert validate_experiment(180, 35, 9) is True
    assert validate_experiment(-10, 0, 15) is False


def test_get_experiment_result() -> None:
    assert get_experiment_result(True, 9) == "Эксперимент успешный"
    assert get_experiment_result(True, 6) == "Результат удовлетворительный"
    assert get_experiment_result(True, 3) == "Эксперимент неудачный"
    assert get_experiment_result(False, 9) == "Эксперимент заполнен некорректно"


def test_build_experiment_preview() -> None:
    preview = build_experiment_preview(
        "Шоколадный кекс",
        "Уменьшено количество сахара на 20%",
        180,
        35,
        9,
        "Эксперимент успешный",
    )
    assert "Рецепт: Шоколадный кекс" in preview
    assert "Оценка вкуса: 9/10" in preview
    assert "Результат: Эксперимент успешный" in preview
