# ПР9 — результаты и матрица ORM

Дата проверки: 2 ноября 2026 года. Автор: Калугин Никита Александрович, ЭФБО-12-24.
Индивидуальная тема: «Система учета кулинарных экспериментов».
Основание: PR9_Django_ORM_modeli.pdf, разделы 2, 5, 6, 7.4.

## Контрольная точка

ПР9 начата с чистого main `0ec1325` в ветке pr9-django-orm.
До изменений: Django check и flake8 без ошибок, 17 тестов пройдены.

## Реализованные выражения

| № | Назначение | Реализация |
| --- | --- | --- |
| 1 | Набор рецептов и число опытов | web_recipes/queries.py recipe_catalog annotate Count |
| 2 | Карточка рецепта по ID | web_recipes/views.py recipe_detail filter first |
| 3 | Один участник | db/repository.py save_user objects.get |
| 4 | Фильтр категории | recipe_catalog category__icontains |
| 5 | Поиск названия | recipe_catalog name__icontains |
| 6 | Поиск описания рецепта автора | experiment_catalog Q с тремя условиями OR |
| 7 | Фильтр оценки связанной модели | experiment_catalog result__taste_score__gte |
| 8 | Фильтр рецепта | experiment_catalog filter recipe |
| 9 | Фильтр даты совместно с оценкой | experiment_catalog filter experiment_date после фильтра оценки |
| 10 | Исключение отменённых | experiment_catalog exclude is_cancelled |
| 11 | Выбор отменённых | experiment_catalog filter is_cancelled |
| 12 | Сортировка названия | recipe_catalog order_by name id |
| 13 | Сортировка даты и ID | experiment_catalog newest oldest |
| 14 | Сортировка поля рецепта | experiment_catalog recipe__name -experiment_date -id |
| 15 | Связанные объекты одним запросом | experiment_catalog select_related recipe user result |
| 16 | Обратные связи | Recipe.experiments User.experiments; console и tests/test_orm.py |
| 17 | Среднее по всем результатам | dashboard_stats aggregate Avg |
| 18 | Группировка категорий | recipe_categories values category annotate Count |
| 19 | Сводка оценок | experiment_statistics aggregate Count Avg Min Max |
| 20 | Общее время | experiment_statistics aggregate Sum duration_minutes |
| 21 | Сводка рецептов включая нулевые | experiment_statistics Recipe annotate Count Avg |
| 22 | Группировка статусов с отменой | experiment_statistics Case When values annotate |
| 23 | Последние три опыта | homepage/views.py QuerySet slice [:3] |
| 24 | Постраничная выборка | web_experiments/views.py Paginator get_page |
| 25 | Создание | db/repository.py save_recipe save_experiment full_clean save |
| 26 | Обновление | cancel_saved_experiment filter update; Experiment.cancel save |
| 27 | Удаление с каскадом результата | delete_saved_experiment filter delete |

Выражения используются в представлениях, адаптере консоли и защите; регрессии
проверяют поведение и обратные связи. Сортировка перед пагинацией стабилизирована ID.

## Перенос

Источник — data/culinary_lab.sqlite. Назначение — data/culinary_orm.sqlite3.
Начальные миграции созданы отдельно для web_recipes и web_experiments.
Перенесены 1 пользователь, 2 рецепта, 1 эксперимент и 1 результат. Проверены
все значения всех строк и связей; SHA-256 источника до и после одинаков.
Повторный импорт в непустую базу запрещён. Ошибочная дата в источнике приводит
к полному откату, включая уже вставленных пользователей и рецепты.

## Проверки

- python manage.py check — 0 ошибок.
- python manage.py makemigrations --check --dry-run — No changes detected.
- python manage.py showmigrations — миграции применены, в том числе обе миграции приложений.
- python -m pytest -v — 33 passed, отдельная тестовая база.
- python -m flake8 . --extend-exclude=venv — без замечаний.
- python scripts/smoke_test.py — реальный сервер, 19 HTTP-проверок страниц,
  поиска и статики, создание рецепта и опыта из консоли, видимость на работающем сайте.
- Браузер Microsoft Edge — 7 страниц, форма с шестью фильтрами, переход
  вперёд и назад с сохранением параметров, 5 карточек на странице,
  переключатель контраста, ширина 1440 и 390 px, отсутствие ошибок JavaScript.

Сценарий доступных помещений из примера Roomly заменён предметной областью
кулинарных опытов: отмена сохраняет историю и исключается фильтром «Действующие».
Рецепты не являются бронируемым ресурсом, календарные блокировки им не добавлялись.

Яндекс Практикум: все 12 материалов ПР9 выполнены и показаны преподавателю,
согласно подтверждению студента; полный перечень приведён в CHECKLIST.md.
