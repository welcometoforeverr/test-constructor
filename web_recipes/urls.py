"""Recipe URL routes."""
from django.urls import path
from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("<int:recipe_id>/", views.recipe_detail, name="detail"),
]
