# CulinaryLab — система учета кулинарных экспериментов

Сквозной учебный проект **Калугина Никиты Александровича, ЭФБО-12-24**
по дисциплине «Технологии разработки приложений на базе фреймворков».
Преподаватель: Ящун Татьяна Викторовна.

## Этапы разработки

- **ПР1:** базовый консольный сценарий.
- **ПР2:** коллекции, модули, JSON, исключения и тесты.
- **ПР3:** объектная модель User, Recipe, Experiment, ExperimentResult.
- **ПР5:** Django 5.2, HTTP, маршруты и view-функции.
- **ПР6:** Django templates, context, include и static.
- **ПР7:** SQLite, SQL, sqlite3 и вывод результатов SQL в Django.

Предыдущая JSON-реализация сохранена. В ПР7 Django ORM ещё не используется:
база доступна напрямую через стандартный модуль `sqlite3`.

## База данных ПР7

Файл базы после импорта: `data/culinary_lab.sqlite`.

Схема хранится в `sql/schema.sql` и содержит четыре таблицы:

- `users(id, name, email)`;
- `recipes(id, name, category)`;
- `experiments(id, user_id, recipe_id, change_description,
  temperature, duration_minutes, experiment_date, is_cancelled)`;
- `experiment_results(id, experiment_id, taste_score, status)`.

Первичные ключи — поля `id`. Внешние ключи связывают experiment с
пользователем и рецептом, а experiment_results — с experiment.

## Перенос JSON → SQLite

`db/database.py` создаёт подключение через `sqlite3.connect()`, включает
`PRAGMA foreign_keys = ON` и использует `sqlite3.Row`.

`db/import_json.py` создаёт схему и переносит данные из JSON через
параметризованные INSERT и `executemany()`.

После клонирования база создаётся командой:

```bash
python -m db.import_json
```

Если файла базы ещё нет, веб-слой также умеет автоматически восстановить его
из JSON при первом обращении.

## SQL-запросы

В `sql/queries.sql` сохранено **14 запросов**, включая:

- обычные SELECT-выборки;
- фильтрацию через WHERE;
- JOIN между связанными таблицами;
- COUNT, AVG, MIN, MAX;
- GROUP BY;
- HAVING;
- сортировку ORDER BY.

Пользовательские значения не вставляются через f-строки. В Python используются
плейсхолдеры `?`.

## Django и SQLite

Веб-страницы ПР7 получают данные через `db/queries.py`:

- `/` — сводные показатели SQLite;
- `/recipes/` — рецепты, поиск по названию и категории;
- `/recipes/categories/` — GROUP BY по категориям;
- `/recipes/<id>/` — рецепт и агрегированная статистика;
- `/experiments/` — JOIN и фильтр по минимальной оценке;
- `/experiments/statistics/` — COUNT/AVG и GROUP BY;
- `/experiments/<id>/` — полная связанная информация об эксперименте.

Путь данных ПР7:

`SQLite → SQL → sqlite3 → Django view → context → template → HTML`.

## Запуск

Рекомендуется Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m db.import_json
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py runserver
```

Открыть: **http://127.0.0.1:8000/**.

## Проверка

```bash
python manage.py check
python -m pytest -v
python -m flake8 . --extend-exclude=venv,.venv
```

Прохождение материалов Яндекс Практикума подтверждается отдельно в личном
кабинете.
