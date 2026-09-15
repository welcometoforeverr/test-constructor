# Отладка проекта в VS Code / PyCharm

Для ПР1 преподавателю нужно показать breakpoint, пошаговое выполнение и просмотр значений переменных.

## Что показать

1. Откройте `main.py`.
2. Поставьте breakpoint на строке:
   ```python
   title_is_valid = validate_test_title(test_title)
   ```
3. Запустите `main.py` в режиме **Debug**.
4. После остановки посмотрите значения:
   - `teacher_name`;
   - `test_title`;
   - `question_text`;
   - `correct_variant`;
   - `is_published`.
5. Выполните несколько шагов **Step Over** и проследите появление значений `title_is_valid`, `question_is_valid`, `status` и `preview`.

## Упражнение с ошибкой

Для демонстрации поиска дефекта временно замените в функции `validate_test_title()` строку:

```python
return len(cleaned_title) >= 3
```

на ошибочную:

```python
return len(cleaned_title) < 3
```

После этого корректное название `"Основы Python"` станет считаться неправильным, а статус теста изменится на сообщение о невозможности публикации.

Через breakpoint внутри `validate_test_title()` видно, что `cleaned_title` заполнен правильно, но условие сравнения записано наоборот. Верните `>= 3` и повторно запустите программу.

**В итоговом проекте ошибка уже исправлена.**
