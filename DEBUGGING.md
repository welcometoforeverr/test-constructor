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

## ПР10–ПР11

После git pull: python -m pip install -r requirements.txt; python manage.py migrate;
python manage.py createsuperuser; python manage.py runserver.
Откройте /admin/, найдите эксперимент по названию рецепта, примените фильтр,
покажите inline в карточке рецепта. Для Debug Toolbar установите переменную
CULINARY_DEBUG_TOOLBAR=1 до запуска сервера и откройте вкладку SQL.
На /experiments/create/ создайте опыт, введите оценку 11 и убедитесь в ошибке.
Исправьте оценку, сохраните, отредактируйте и отмените через POST.
На /recipes/create/ загрузите PNG/JPEG и откройте карточку рецепта.
Снимки этих действий и терминала нужны для отчётов по методичкам.
