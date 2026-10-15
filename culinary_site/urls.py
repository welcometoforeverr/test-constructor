"""Project-level URL routing."""
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("recipes/", include("web_recipes.urls")),
    path("experiments/", include("web_experiments.urls")),
]
