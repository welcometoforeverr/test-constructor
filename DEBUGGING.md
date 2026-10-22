# Проверка ПР7

1. Подтянуть изменения: `git pull`.
2. Установить зависимости: `python -m pip install -r requirements.txt`.
3. Пересоздать БД: `python -m db.import_json`.
4. Открыть `data/culinary_lab.sqlite` в SQLite Viewer.
5. Проверить таблицы: users, recipes, experiments, experiment_results.
6. Открыть `sql/queries.sql` и показать SELECT, WHERE, JOIN, COUNT, GROUP BY.
7. Поставить breakpoint в `db/queries.py` на `connection.execute()`.
8. Открыть `/experiments/?min_score=8` и показать параметризированный запрос.
9. Открыть `/experiments/statistics/` и показать результат агрегатов.
10. Выполнить:
    - `python manage.py check`;
    - `python -m pytest -v`;
    - `python -m flake8 . --extend-exclude=venv,.venv`.
