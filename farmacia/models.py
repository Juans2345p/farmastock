"""
Modelos del proyecto Farma.

Cada modelo declara `db_table` con el nombre exacto solicitado en el esquema
SQLite (MEDICO, PACIENTE, MEDICAMENTO, SEDES, RECETA, RECETA_MEDICAMENTO y
ALMACEN). Los tipos de columna también se ajustan al esquema entregado.
"""
from django.db import models


class SQLiteDateTextField(models.DateField):
    """
    DateField almacenado como TEXT en SQLite.

    El esquema académico define RECETA.fecha como TEXT. Django, por defecto,
    generaría una columna de tipo "date"; esta subclase conserva toda la
    funcionalidad de DateField (admin, formularios, serializers, filtros) y
    solo cambia el tipo de columna creado en SQLite.
    """

    def db_type(self, connection):
        if connection.vendor == "sqlite":
            return "text"
        return super().db_type(connection)


class Medico(models.Model):
    nombre = models.TextField()

    class Meta:
        db_table = "MEDICO"
        verbose_name = "médico"
        verbose_name_plural = "médicos"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.TextField()

    class Meta:
        db_table = "PACIENTE"
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    nombre = models.TextField()
    tipo = models.TextField()
    gramos = models.FloatField()

    class Meta:
        db_table = "MEDICAMENTO"
        verbose_name = "medicamento"
        verbose_name_plural = "medicamentos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.nombre} ({self.gramos:g} g)"


class Sede(models.Model):
    nombre = models.TextField(unique=True)
    direccion = models.TextField()

    class Meta:
        db_table = "SEDES"
        verbose_name = "sede"
        verbose_name_plural = "sedes"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        db_column="medico_id",
        related_name="recetas",
        verbose_name="médico",
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        db_column="paciente_id",
        related_name="recetas",
        verbose_name="paciente",
    )
    fecha = SQLiteDateTextField(verbose_name="fecha")

    class Meta:
        db_table = "RECETA"
        verbose_name = "receta"
        verbose_name_plural = "recetas"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"Receta #{self.pk} — {self.paciente}"


class RecetaMedicamento(models.Model):
    receta = models.ForeignKey(
        Receta,
        on_delete=models.CASCADE,
        db_column="receta_id",
        related_name="detalles",
        verbose_name="receta",
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.PROTECT,
        db_column="medicamento_id",
        related_name="detalles_receta",
        verbose_name="medicamento",
    )
    cantidad = models.IntegerField()

    class Meta:
        db_table = "RECETA_MEDICAMENTO"
        verbose_name = "medicamento de la receta"
        verbose_name_plural = "medicamentos de la receta"
        ordering = ["id"]

    def __str__(self):
        return f"{self.medicamento} × {self.cantidad}"


class Almacen(models.Model):
    sede = models.ForeignKey(
        Sede,
        on_delete=models.PROTECT,
        db_column="sede_id",
        related_name="inventario",
        verbose_name="sede",
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.PROTECT,
        db_column="medicamento_id",
        related_name="inventario",
        verbose_name="medicamento",
    )
    cajas = models.IntegerField()

    class Meta:
        db_table = "ALMACEN"
        verbose_name = "registro de almacén"
        verbose_name_plural = "almacén"
        ordering = ["id"]

    def __str__(self):
        return f"{self.sede} — {self.medicamento} ({self.cajas} cajas)"
