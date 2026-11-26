"""Vistas de la API REST y vista HTML de la fórmula médica con QR."""
import base64
from io import BytesIO

import qrcode
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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


def index(request):
    """Portada sencilla del proyecto Farma."""
    receta_ejemplo = Receta.objects.order_by("id").first()
    contexto = {
        "receta_ejemplo": receta_ejemplo.pk if receta_ejemplo else 1,
        "total_medicos": Medico.objects.count(),
        "total_pacientes": Paciente.objects.count(),
        "total_medicamentos": Medicamento.objects.count(),
        "total_recetas": Receta.objects.count(),
    }
    return render(request, "farmacia/index.html", contexto)


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


def _url_publica_receta(request, receta) -> str:
    """
    Construye la URL que se codifica en el QR.

    Si FARMA_PUBLIC_URL está definida, se usa esa base (útil para IP de la LAN
    o dominio). Si está vacía, se usa el host con el que se abrió la página.
    """
    ruta = reverse("receta-formula", args=[receta.pk])
    base = getattr(settings, "FARMA_PUBLIC_URL", "").strip().rstrip("/")

    if base:
        if "://" not in base:
            base = f"http://{base}"
        return f"{base}{ruta}"

    return request.build_absolute_uri(ruta)


def _generar_qr_base64(contenido: str) -> str:
    """Genera un PNG con el código QR y lo devuelve codificado en Base64."""
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

    qr_url = _url_publica_receta(request, receta)
    contexto = {
        "receta": receta,
        "qr_url": qr_url,
        "qr_base64": _generar_qr_base64(qr_url),
    }
    return render(request, "farmacia/receta_formula.html", contexto)
