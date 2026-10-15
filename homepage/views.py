"""PR5: respond to HTTP requests with HTML built in Python."""
from django.http import HttpResponse
from django.utils.html import format_html

from web_data import get_catalog


def page(title: str, content: str) -> HttpResponse:
    """Render a simple HTML shell; PR6 will replace it with templates."""
    return HttpResponse(format_html(
        "<!DOCTYPE html><html lang='ru'><head>"
        "<meta charset='utf-8'><meta name='viewport' "
        "content='width=device-width, initial-scale=1'>"
        "<title>{}</title>"
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/"
        "bootstrap@5.3.3/dist/css/bootstrap.min.css'></head>"
        "<body><nav class='container py-3 d-flex gap-3'>"
        "<a href='/'>Главная</a><a href='/recipes/'>Рецепты</a>"
        "<a href='/experiments/'>Эксперименты</a></nav>"
        "<main class='container py-4'>{}</main></body></html>",
        title,
        content,
    ))


def index(request):
    """Home page and current project statistics."""
    users, recipes, experiments = get_catalog()
    content = format_html(
        "<h1>Кулинарные эксперименты</h1>"
        "<p>Рецептов: {}. Экспериментов: {}. Пользователей: {}.</p>"
        "<p>Начало веб-версии сквозного проекта (ПР5).</p>",
        len(recipes),
        len(experiments),
        len(users),
    )
    return page("Кулинарные эксперименты", content)
