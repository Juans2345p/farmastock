"""Serializers de la API REST del proyecto Farma."""
from rest_framework import serializers

from .models import (
    Almacen,
    Medico,
    Medicamento,
    Paciente,
    Receta,
    RecetaMedicamento,
    Sede,
)


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ["id", "nombre"]


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ["id", "nombre"]


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ["id", "nombre", "tipo", "gramos"]


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ["id", "nombre", "direccion"]


class RecetaMedicamentoSerializer(serializers.ModelSerializer):
    """Serializer completo para el CRUD de /api/receta-medicamentos/."""

    medicamento_nombre = serializers.CharField(
        source="medicamento.nombre", read_only=True
    )
    medicamento_tipo = serializers.CharField(
        source="medicamento.tipo", read_only=True
    )
    medicamento_gramos = serializers.FloatField(
        source="medicamento.gramos", read_only=True
    )

    class Meta:
        model = RecetaMedicamento
        fields = [
            "id",
            "receta",
            "medicamento",
            "medicamento_nombre",
            "medicamento_tipo",
            "medicamento_gramos",
            "cantidad",
        ]


class RecetaMedicamentoDetalleSerializer(serializers.ModelSerializer):
    """Detalle anidado (solo lectura) dentro de una receta."""

    nombre = serializers.CharField(source="medicamento.nombre", read_only=True)
    tipo = serializers.CharField(source="medicamento.tipo", read_only=True)
    gramos = serializers.FloatField(source="medicamento.gramos", read_only=True)

    class Meta:
        model = RecetaMedicamento
        fields = ["id", "medicamento", "nombre", "tipo", "gramos", "cantidad"]
        read_only_fields = fields


class RecetaSerializer(serializers.ModelSerializer):
    """Receta con el detalle anidado de sus medicamentos."""

    medico_nombre = serializers.CharField(source="medico.nombre", read_only=True)
    paciente_nombre = serializers.CharField(
        source="paciente.nombre", read_only=True
    )
    medicamentos = RecetaMedicamentoDetalleSerializer(
        source="detalles", many=True, read_only=True
    )

    class Meta:
        model = Receta
        fields = [
            "id",
            "medico",
            "medico_nombre",
            "paciente",
            "paciente_nombre",
            "fecha",
            "medicamentos",
        ]


class AlmacenSerializer(serializers.ModelSerializer):
    sede_nombre = serializers.CharField(source="sede.nombre", read_only=True)
    medicamento_nombre = serializers.CharField(
        source="medicamento.nombre", read_only=True
    )

    class Meta:
        model = Almacen
        fields = [
            "id",
            "sede",
            "sede_nombre",
            "medicamento",
            "medicamento_nombre",
            "cajas",
        ]
