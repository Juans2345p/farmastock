"""Rutas principales del proyecto Farma."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Incluye /api/... y /receta/<id>/
    path("", include("farmacia.urls")),
]
