# Проверка и отладка ПР5 и ПР6

1. Установите зависимости: `python -m pip install -r requirements.txt`.
2. Выполните `python manage.py check`.
3. Запустите сервер: `python manage.py runserver`.
4. Проверьте `/`, `/recipes/`, `/recipes/1/`, `/experiments/`, `/experiments/1/`.
5. Откройте `/recipes/9999/` — ожидается статус HTTP 404 и шаблон «Рецепт не найден».
6. Откройте `/experiments/9999/` — аналогичная проверка 404.
7. В `web_recipes/views.py` поставьте breakpoint на вызове `get_recipes()` и проследите передачу объектов в контекст.
8. В `templates/base.html` покажите `extends` в дочернем шаблоне, `block` и `include` навигации.
9. В `static/homepage/css/style.css` временно измените цвет акцента и обновите страницу.
10. Кнопка «Контраст» в меню вызывает обработчик `static/homepage/js/main.js`.
11. Проверьте код командой `python -m flake8 . --extend-exclude=venv,.venv`, тесты — `python -m pytest -v`.
