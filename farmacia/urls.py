"""Rutas de la aplicación farmacia: API REST y fórmula médica."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AlmacenViewSet,
    MedicoViewSet,
    MedicamentoViewSet,
    PacienteViewSet,
    RecetaMedicamentoViewSet,
    RecetaViewSet,
    SedeViewSet,
    receta_formula,
)

router = DefaultRouter()
router.register("medicos", MedicoViewSet, basename="medico")
router.register("pacientes", PacienteViewSet, basename="paciente")
router.register("medicamentos", MedicamentoViewSet, basename="medicamento")
router.register("sedes", SedeViewSet, basename="sede")
router.register("recetas", RecetaViewSet, basename="receta")
router.register(
    "receta-medicamentos", RecetaMedicamentoViewSet, basename="receta-medicamento"
)
router.register("almacen", AlmacenViewSet, basename="almacen")

urlpatterns = [
    path("api/", include(router.urls)),
    path("receta/<int:id>/", receta_formula, name="receta-formula"),
]
