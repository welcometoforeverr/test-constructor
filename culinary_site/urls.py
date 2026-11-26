"""Project-level URL routing."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("recipes/", include("web_recipes.urls")),
    path("experiments/", include("web_experiments.urls")),
]

if settings.SHOW_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
