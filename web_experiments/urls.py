"""Experiment URL routes."""
from django.urls import path
from . import views

app_name = "experiments"
urlpatterns = [
    path("", views.experiment_list, name="list"),
    path("<int:experiment_id>/", views.experiment_detail, name="detail"),
]
