"""Configuración del Django Admin para gestionar todos los datos."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Almacen,
    Medico,
    Medicamento,
    Paciente,
    Receta,
    RecetaMedicamento,
    Sede,
)

admin.site.site_header = "Farma · Administración"
admin.site.site_title = "Farma"
admin.site.index_title = "Gestión de médicos, pacientes, recetas e inventario"


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("id",)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("id",)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo", "gramos")
    list_filter = ("tipo",)
    search_fields = ("nombre", "tipo")
    ordering = ("id",)


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "direccion")
    search_fields = ("nombre", "direccion")
    ordering = ("id",)


class RecetaMedicamentoInline(admin.TabularInline):
    """Permite agregar/quitar medicamentos directamente desde la receta."""

    model = RecetaMedicamento
    fields = ("medicamento", "cantidad")
    autocomplete_fields = ("medicamento",)
    extra = 1
    show_change_link = True


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ("id", "medico", "paciente", "fecha", "ver_formula")
    list_display_links = ("id",)
    list_filter = ("fecha", "medico")
    search_fields = ("id", "medico__nombre", "paciente__nombre")
    autocomplete_fields = ("medico", "paciente")
    date_hierarchy = "fecha"
    list_select_related = ("medico", "paciente")
    inlines = [RecetaMedicamentoInline]
    save_on_top = True

    @admin.display(description="Fórmula")
    def ver_formula(self, obj):
        """Enlace directo desde el listado a la vista de impresión/captura."""
        url = reverse("receta-formula", args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">Ver fórmula</a>',
            url,
        )


@admin.register(RecetaMedicamento)
class RecetaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "receta", "medicamento", "cantidad")
    list_filter = ("medicamento",)
    search_fields = ("receta__id", "medicamento__nombre")
    autocomplete_fields = ("receta", "medicamento")
    list_select_related = ("receta", "medicamento")
    ordering = ("id",)


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ("id", "sede", "medicamento", "cajas")
    list_filter = ("sede", "medicamento")
    search_fields = ("sede__nombre", "medicamento__nombre")
    autocomplete_fields = ("sede", "medicamento")
    list_select_related = ("sede", "medicamento")
    ordering = ("id",)
