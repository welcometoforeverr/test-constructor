"""Validated GET parameters; invalid input never becomes a field name."""

from django import forms

from web_recipes.models import Recipe
from .models import User
from .queries import SORTS


class ExperimentFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Поиск", max_length=200)
    min_score = forms.IntegerField(
        required=False, min_value=1, max_value=10, label="Минимальная оценка"
    )
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(), required=False, label="Рецепт"
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False, label="Участник"
    )
    date = forms.DateField(
        required=False, label="Дата", widget=forms.DateInput(attrs={"type": "date"})
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=[
            ("", "Все"),
            ("active", "Действующие"),
            ("cancelled", "Отменённые"),
        ],
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=list(
            zip(SORTS, ["Сначала новые", "Сначала старые", "По оценке", "По рецепту"])
        ),
    )
