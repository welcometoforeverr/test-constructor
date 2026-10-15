# CulinaryLab — система учета кулинарных экспериментов

Сквозной учебный проект **Калугина Никиты Александровича, ЭФБО-12-24**, по дисциплине «Технологии разработки приложений на базе фреймворков». Преподаватель: Ящун Татьяна Викторовна.

## Этапы разработки

- **ПР1:** базовый консольный сценарий.
- **ПР2:** коллекции, модули, JSON, исключения, тесты.
- **ПР3:** объектная модель `User`, `Recipe`, `Experiment`, `ExperimentResult`.
- **ПР5:** Django 5.2, HTTP, URL, view-функции, пять веб-страниц.
- **ПР6:** шаблоны Django, `render()`, контекст, наследование, `include`, именованные URL, фильтры и собственные статические файлы.

Код консольной версии (`main.py`) и JSON-объекты из ПР3 сохранены. **Django ORM пока не используется** — это предусмотрено для следующих практик.

## Django-проект и приложения

- `culinary_site/` — настройки и корневой URLconf.
- `homepage/` — главная страница, статистика.
- `web_recipes/` — список рецептов и страница отдельного рецепта.
- `web_experiments/` — список экспериментов и страница отдельного эксперимента.
- `templates/base.html` — общий HTML-каркас.
- `templates/includes/navigation.html` — общая навигация.
- `web_recipes/templates/recipes/` — шаблоны рецептов и include карточки.
- `web_experiments/templates/experiments/` — шаблоны экспериментов и include статуса.
- `static/homepage/` — собственные CSS, JavaScript и SVG-логотип.
- `web_data.py` — мост между Django и существующим JSON/ООП.
- `models/`, `storage.py`, `data/` — сохраненная предметная область ПР3.
- `tests/` — тестирование кода и HTTP-страниц.

Имена `web_recipes` и `web_experiments` выбраны во избежание конфликта с существующими модулями `recipes.py` и `experiments.py`.

## URL-маршруты

| Страница | URL | Имя маршрута |
|---|---|---|
| Главная | `/` | `homepage:index` |
| Рецепты | `/recipes/` | `recipes:list` |
| Отдельный рецепт | `/recipes/1/` | `recipes:detail` |
| Эксперименты | `/experiments/` | `experiments:list` |
| Отдельный эксперимент | `/experiments/1/` | `experiments:detail` |

Для неизвестного идентификатора detail-view возвращает HTTP **404** и отображает сообщение в соответствующем шаблоне. Веб-интерфейс на данном этапе доступен только для просмотра; добавление и редактирование сохраняются в консольной версии до появления Django Forms.

## Архитектура ПР6

Браузер → Django URLconf → view → JSON/объекты Python → context → HTML-шаблон → HTTP-ответ.

- `{% extends %}` и `{% block %}` — наследование базового шаблона.
- `{% include %}` — карточки, статус, навигация.
- `{{ value }}`, `{% for %}`, `{% if %}`, `{% empty %}` — вывод данных.
- `{% url 'recipes:detail' recipe.id %}` — именованный URL.
- `|default`, `|truncatechars`, `|length` — фильтры.
- `{% load static %}` и `{% static %}` — загрузка CSS, JS и изображения.

Формирование HTML внутри Python через функцию `page()` из ПР5 полностью удалено.

## Установка и запуск

Рекомендуется Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.venv\\Scripts\\python.exe manage.py check
.venv\\Scripts\\python.exe manage.py runserver
```

Адрес сайта: **http://127.0.0.1:8000/**.

## Тестирование

```bash
python manage.py check
python -m pytest -v
python -m flake8 . --extend-exclude=venv,.venv
```

Результаты проверяются по выводу команд. Прохождение материалов Яндекс Практикума подтверждается в личном кабинете отдельно.
