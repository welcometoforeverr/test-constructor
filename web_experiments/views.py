"""PR5: experiment HTTP views with direct HTML output."""
from django.http import HttpResponse
from django.utils.html import format_html, format_html_join

from homepage.views import page
from web_data import get_catalog


def experiment_list(request):
    """List the experiments saved in JSON."""
    _, _, experiments = get_catalog()
    items = format_html_join(
        "",
        "<li class='list-group-item'><a href='/experiments/{}/'>"
        "Эксперимент №{}</a> — {} — {}</li>",
        (
            (item.id, item.id, item.recipe.name, item.status)
            for item in experiments
        ),
    )
    if not experiments:
        items = format_html("<li>Экспериментов пока нет</li>")
    return page("Эксперименты", format_html(
        "<h1>Эксперименты</h1><ul class='list-group'>{}</ul>", items
    ))


def experiment_detail(request, experiment_id: int) -> HttpResponse:
    """Display one experiment or return HTTP 404."""
    _, _, experiments = get_catalog()
    item = next(
        (row for row in experiments if row.id == experiment_id),
        None,
    )
    if item is None:
        response = page("Не найдено", format_html(
            "<h1>Эксперимент не найден</h1>"
        ))
        response.status_code = 404
        return response
    return page("Эксперимент", format_html(
        "<h1>Эксперимент №{}</h1><p>Рецепт: {}</p>"
        "<p>Автор: {}</p><p>Изменение: {}</p>"
        "<p>Температура: {} °C, время: {} мин</p>"
        "<p>Оценка: {}/10, статус: {}</p>"
        "<a href='/experiments/'>К списку экспериментов</a>",
        item.id, item.recipe.name, item.user.name, item.change,
        item.temperature, item.duration_minutes,
        item.result.taste_score, item.status,
    ))
