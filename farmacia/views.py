"""Vistas de la API REST y vista HTML de la fórmula médica con QR."""
import base64
from io import BytesIO

import qrcode
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from .models import (
    Almacen,
    Medico,
    Medicamento,
    Paciente,
    Receta,
    RecetaMedicamento,
    Sede,
)
from .serializers import (
    AlmacenSerializer,
    MedicoSerializer,
    MedicamentoSerializer,
    PacienteSerializer,
    RecetaMedicamentoSerializer,
    RecetaSerializer,
    SedeSerializer,
)


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer


class RecetaViewSet(viewsets.ModelViewSet):
    queryset = (
        Receta.objects.select_related("medico", "paciente")
        .prefetch_related("detalles__medicamento")
        .all()
    )
    serializer_class = RecetaSerializer


class RecetaMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = RecetaMedicamento.objects.select_related(
        "receta", "medicamento"
    ).all()
    serializer_class = RecetaMedicamentoSerializer


class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.select_related("sede", "medicamento").all()
    serializer_class = AlmacenSerializer


def _generar_qr_base64(contenido: str) -> str:
    """
    Genera un PNG con el código QR y lo devuelve codificado en Base64.

    El contenido debe ser únicamente el ID de la receta; la vista se encarga
    de pasar `str(receta.id)`.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(contenido)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="#0f172a", back_color="white")
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def receta_formula(request, id):
    """Vista HTML de la fórmula médica, lista para captura o impresión."""
    receta = get_object_or_404(
        Receta.objects.select_related("medico", "paciente").prefetch_related(
            "detalles__medicamento"
        ),
        pk=id,
    )

    contexto = {
        "receta": receta,
        # Regla estricta: el QR contiene SOLO el ID numérico, sin URL ni texto.
        "qr_base64": _generar_qr_base64(str(receta.id)),
    }
    return render(request, "farmacia/receta_formula.html", contexto)
