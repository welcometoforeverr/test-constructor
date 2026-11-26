"""Validated GET parameters; invalid input never becomes a field name."""

from django import forms
from django.utils import timezone

from web_recipes.models import Recipe
from .models import Experiment, User
from .queries import SORTS


class ExperimentFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                'form-select' if isinstance(field.widget, forms.Select)
                else 'form-control'
            )

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


class ExperimentForm(forms.ModelForm):
    taste_score = forms.IntegerField(
        label="Оценка вкуса (1–10)", min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Experiment
        fields = (
            "user", "recipe", "change_description", "temperature",
            "duration_minutes", "experiment_date",
        )
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "recipe": forms.Select(attrs={"class": "form-select"}),
            "change_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "temperature": forms.NumberInput(attrs={"class": "form-control"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "experiment_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and hasattr(self.instance, "result"):
            self.fields["taste_score"].initial = self.instance.result.taste_score

    def clean_experiment_date(self):
        day = self.cleaned_data["experiment_date"]
        if day > timezone.localdate():
            raise forms.ValidationError("Нельзя записать результат будущего опыта.")
        return day

    def clean_change_description(self):
        change = self.cleaned_data["change_description"].strip()
        if not change:
            raise forms.ValidationError("Опишите, что изменилось в рецепте.")
        return change

    def clean(self):
        data = super().clean()
        if self.instance.pk and self.instance.is_cancelled:
            raise forms.ValidationError("Отменённый эксперимент нельзя редактировать.")
        return data
