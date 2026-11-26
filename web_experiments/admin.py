"""Localized administrative views and related objects."""

from django.contrib import admin

from .models import Experiment, ExperimentResult, User


class ExperimentInline(admin.TabularInline):
    model = Experiment
    extra = 0
    fields = ("recipe", "user", "experiment_date", "is_cancelled")
    readonly_fields = fields
    show_change_link = True
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class ResultInline(admin.StackedInline):
    model = ExperimentResult
    extra = 1
    min_num = 1
    max_num = 1
    can_delete = False

    def get_formset(self, request, obj=None, **kwargs):
        kwargs["validate_min"] = True
        return super().get_formset(request, obj, **kwargs)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    ordering = ("name", "id")
    inlines = [ExperimentInline]
    list_per_page = 20


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "user", "experiment_date", "is_cancelled", "status")
    list_display_links = ("id", "recipe")
    search_fields = ("recipe__name", "user__name", "change_description")
    list_filter = ("is_cancelled", "experiment_date", "recipe", "user")
    ordering = ("-experiment_date", "-id")
    list_select_related = ("recipe", "user", "result")
    inlines = [ResultInline]
    list_per_page = 20


@admin.register(ExperimentResult)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("experiment", "taste_score", "status")
    list_filter = ("status", "taste_score")
    search_fields = ("experiment__recipe__name", "experiment__user__name")
    list_select_related = ("experiment",)
    ordering = ("-taste_score", "id")

    def has_delete_permission(self, request, obj=None):
        # Keep the required result; deleting an experiment cascades instead.
        return False
