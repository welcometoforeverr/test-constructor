"""PR5: recipe HTTP views with direct HTML output."""
from django.http import HttpResponse
from django.utils.html import format_html, format_html_join

from homepage.views import page
from web_data import get_recipes


def recipe_list(request):
    """List the available recipe objects."""
    recipes = get_recipes()
    items = format_html_join(
        "",
        "<li class='list-group-item'><a href='/recipes/{}/'>{}</a>"
        " <span class='text-secondary'>— {}</span></li>",
        ((recipe.id, recipe.name, recipe.category) for recipe in recipes),
    )
    if not recipes:
        items = format_html("<li>Рецептов пока нет</li>")
    return page("Рецепты", format_html(
        "<h1>Рецепты</h1><ul class='list-group'>{}</ul>", items
    ))


def recipe_detail(request, recipe_id: int) -> HttpResponse:
    """Display one recipe or the correct HTTP 404 status."""
    recipe = next(
        (item for item in get_recipes() if item.id == recipe_id),
        None,
    )
    if recipe is None:
        response = page("Не найдено", format_html(
            "<h1>Рецепт не найден</h1>"
        ))
        response.status_code = 404
        return response
    return page(recipe.name, format_html(
        "<h1>{}</h1><p>Категория: {}</p>"
        "<a href='/recipes/'>К списку рецептов</a>",
        recipe.name,
        recipe.category,
    ))
