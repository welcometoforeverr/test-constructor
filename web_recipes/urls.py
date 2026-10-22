"""Recipe URL routes."""
from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("categories/", views.category_statistics, name="categories"),
    path("<int:recipe_id>/", views.recipe_detail, name="detail"),
]
