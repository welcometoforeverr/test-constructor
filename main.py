"""Начальный сценарий проекта «Конструктор тестов» для ПР1.

Тема проекта: №87 «Конструктор тестов».
Сущности: преподаватель, тест, вопрос, вариант ответа.
"""

from datetime import date


def validate_test_title(title: str) -> bool:
    """Проверить, что название теста можно использовать."""
    cleaned_title = title.strip()
    return len(cleaned_title) >= 3


def validate_question(question_text: str, correct_variant: str) -> bool:
    """Проверить текст вопроса и обозначение правильного варианта."""
    has_text = len(question_text.strip()) >= 5
    valid_variant = (
        correct_variant == "A"
        or correct_variant == "B"
        or correct_variant == "C"
        or correct_variant == "D"
    )
    return has_text and valid_variant


def get_test_status(
    is_published: bool,
    is_title_valid: bool,
    is_question_valid: bool,
) -> str:
    """Вернуть состояние теста на текущем этапе создания."""
    if not is_title_valid:
        return "Нельзя опубликовать: проверьте название теста"
    if not is_question_valid:
        return "Нельзя опубликовать: проверьте вопрос и правильный вариант"
    if is_published:
        return "Тест опубликован"
    return "Тест готов к публикации"


def build_question_preview(
    question_text: str,
    variant_a: str,
    variant_b: str,
    variant_c: str,
    variant_d: str,
    correct_variant: str,
) -> str:
    """Сформировать текстовый предпросмотр созданного вопроса."""
    return (
        f"Вопрос: {question_text}\n"
        f"A. {variant_a}\n"
        f"B. {variant_b}\n"
        f"C. {variant_c}\n"
        f"D. {variant_d}\n"
        f"Правильный вариант: {correct_variant}"
    )


def main() -> None:
    """Показать один законченный сценарий конструктора тестов."""
    teacher_name = "Иванов Иван Иванович"
    test_title = "Основы Python"
    created_at = date.today()
    is_published = False

    # Значение поступает как строка и явно преобразуется в целое число.
    # Это демонстрирует преобразование типов, требуемое в ПР1.
    passing_score_text = "70"
    passing_score = int(passing_score_text)

    question_text = "Какой тип данных используется для целых чисел в Python?"
    variant_a = "int"
    variant_b = "float"
    variant_c = "str"
    variant_d = "bool"
    correct_variant = "A"

    title_is_valid = validate_test_title(test_title)
    question_is_valid = validate_question(question_text, correct_variant)
    status = get_test_status(
        is_published,
        title_is_valid,
        question_is_valid,
    )
    preview = build_question_preview(
        question_text,
        variant_a,
        variant_b,
        variant_c,
        variant_d,
        correct_variant,
    )

    print("=== Конструктор тестов ===")
    print(f"Преподаватель: {teacher_name}")
    print(f"Название теста: {test_title}")
    print(f"Дата создания: {created_at}")
    print(f"Проходной балл: {passing_score}%")
    print(f"Статус: {status}")
    print()
    print(preview)


if __name__ == "__main__":
    main()
