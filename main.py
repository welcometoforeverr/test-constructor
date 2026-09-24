"""Начальный сценарий проекта «Система учета кулинарных экспериментов» для ПР1.

Сущности: пользователь, рецепт, эксперимент, результат.
"""

from datetime import date


def validate_recipe_name(recipe_name: str) -> bool:
    """Проверить, что название рецепта можно использовать."""
    cleaned_name = recipe_name.strip()
    return len(cleaned_name) >= 3


def validate_experiment(temperature: int, duration_minutes: int, taste_score: int) -> bool:
    """Проверить основные параметры кулинарного эксперимента."""
    valid_temperature = temperature > 0
    valid_duration = duration_minutes > 0
    valid_score = 1 <= taste_score <= 10
    return valid_temperature and valid_duration and valid_score


def get_experiment_result(is_valid: bool, taste_score: int) -> str:
    """Определить результат эксперимента."""
    if not is_valid:
        return "Эксперимент заполнен некорректно"
    if taste_score >= 8:
        return "Эксперимент успешный"
    if taste_score >= 5:
        return "Результат удовлетворительный"
    return "Эксперимент неудачный"


def build_experiment_preview(
    recipe_name: str,
    change_description: str,
    temperature: int,
    duration_minutes: int,
    taste_score: int,
    result: str,
) -> str:
    """Сформировать текстовый отчет о кулинарном эксперименте."""
    return (
        f"Рецепт: {recipe_name}\n"
        f"Изменение: {change_description}\n"
        f"Температура: {temperature} °C\n"
        f"Время приготовления: {duration_minutes} мин\n"
        f"Оценка вкуса: {taste_score}/10\n"
        f"Результат: {result}"
    )


def main() -> None:
    """Показать один законченный сценарий учета кулинарного эксперимента."""
    user_name = "Калугин Никита"
    recipe_name = "Шоколадный кекс"
    experiment_date = date.today()

    change_description = "Уменьшено количество сахара на 20%"

    # Параметры получены как строки и преобразуются в числа.
    # Это демонстрирует преобразование типов, требуемое в ПР1.
    temperature_text = "180"
    duration_text = "35"
    taste_score_text = "9"

    temperature = int(temperature_text)
    duration_minutes = int(duration_text)
    taste_score = int(taste_score_text)

    recipe_is_valid = validate_recipe_name(recipe_name)
    experiment_is_valid = validate_experiment(
        temperature,
        duration_minutes,
        taste_score,
    )
    result = get_experiment_result(
        recipe_is_valid and experiment_is_valid,
        taste_score,
    )
    preview = build_experiment_preview(
        recipe_name,
        change_description,
        temperature,
        duration_minutes,
        taste_score,
        result,
    )

    print("=== Система учета кулинарных экспериментов ===")
    print(f"Пользователь: {user_name}")
    print(f"Дата эксперимента: {experiment_date}")
    print()
    print(preview)


if __name__ == "__main__":
    main()
