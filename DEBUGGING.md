# Проверка ПР9

1. Установить зависимости: `python -m pip install -r requirements.txt`.
2. Создать структуру: `python manage.py migrate`.
3. На первом запуске перенести ПР7: `python manage.py import_legacy`.
   Если база не пуста, повторный импорт отказывается менять записи — это штатно.
4. Проверить путь: `python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])"`.
   По умолчанию это `data/culinary_orm.sqlite3`, для сайта и консоли одинаково.
5. Выполнить `python manage.py check`, `python manage.py makemigrations --check`,
   `python manage.py showmigrations`, `python -m pytest -v`, `python -m flake8 . --extend-exclude=venv`.
6. Запустить `python scripts/smoke_test.py` — проверяется живой сервер и синхронизация консоли.
7. Запустить `python manage.py runserver`; открыть `/recipes/`, `/experiments/`,
   `/experiments/statistics/`. Добавить рецепт через `python main.py`, обновить сайт.
8. Для breakpoint использовать `web_experiments/queries.py`: проследить filter →
   order_by → Paginator в views.py, затем связанные объекты в шаблоне.

`no such table` означает, что к выбранной базе не применены миграции.
Пустые списки после migrate ожидаемы до первого переноса.
Проверьте CULINARY_DB_PATH в обоих терминалах, если сайт не видит изменения консоли.
Исторический SQL-слой ПР7 остался для изучения; его команды не нужны для запуска ПР9.
