"""Experiment URL routes."""
from django.urls import path

from . import views

app_name = "experiments"
urlpatterns = [
    path("", views.experiment_list, name="list"),
    path("create/", views.experiment_create, name="create"),
    path("<int:experiment_id>/edit/", views.experiment_edit, name="edit"),
    path("<int:experiment_id>/cancel/", views.experiment_cancel, name="cancel"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:experiment_id>/", views.experiment_detail, name="detail"),
]
