"""Recipe administration and navigation to related experiments."""

from django.contrib import admin

from web_experiments.admin import ExperimentInline
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_display_links = ("id", "name")
    search_fields = ("name", "category")
    list_filter = ("category",)
    ordering = ("name", "id")
    readonly_fields = ("slug",)
    list_per_page = 20
    inlines = [ExperimentInline]


admin.site.site_header = "CulinaryLab — управление данными"
admin.site.site_title = "CulinaryLab"
admin.site.index_title = "Кулинарные эксперименты"
