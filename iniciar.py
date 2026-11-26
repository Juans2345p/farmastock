#!/usr/bin/env python
"""
Script de arranque del proyecto Farma.

En la primera ejecución:
  1. Verifica/instala las dependencias de requirements.txt.
  2. Aplica las migraciones.
  3. Crea el superusuario admin / admin123 si no existe.
  4. Carga datos de prueba (médicos, pacientes, medicamentos, sedes,
     inventario y recetas completas).
  5. Levanta el servidor de desarrollo en http://127.0.0.1:8000/.

Uso:
    python iniciar.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _preparar_entorno() -> None:
    """Asegura dependencias, ruta del proyecto y configuración de Django."""
    try:
        import corsheaders  # noqa: F401
        import django  # noqa: F401
        import PIL  # noqa: F401
        import qrcode  # noqa: F401
        import rest_framework  # noqa: F401
    except ImportError as exc:
        print(f"Falta una dependencia ({exc.name}). Instalando requirements.txt ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(BASE_DIR / "requirements.txt")]
        )

    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farma.settings")

    import django

    django.setup()


def aplicar_migraciones() -> None:
    from django.core.management import call_command

    print("Aplicando migraciones...")
    call_command("migrate", interactive=False, verbosity=1)


def crear_superusuario() -> None:
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if User.objects.filter(username="admin").exists():
        print("El superusuario 'admin' ya existe; no se modifica.")
        return

    User.objects.create_superuser(
        username="admin",
        email="admin@farma.local",
        password="admin123",
    )
    print("Superusuario creado: admin / admin123")


def cargar_datos_prueba() -> None:
    """Carga datos iniciales de forma idempotente."""
    from datetime import date

    from django.db import transaction

    from farmacia.models import (
        Almacen,
        Medico,
        Medicamento,
        Paciente,
        Receta,
        RecetaMedicamento,
        Sede,
    )

    with transaction.atomic():
        medicos = {}
        for nombre in ("Dra. Laura Gómez", "Dr. Carlos Ramírez", "Dra. Ana Torres"):
            medicos[nombre], _ = Medico.objects.get_or_create(nombre=nombre)

        pacientes = {}
        for nombre in ("Juan Pérez", "María Rodríguez", "Andrés Martínez"):
            pacientes[nombre], _ = Paciente.objects.get_or_create(nombre=nombre)

        medicamentos = {}
        datos_medicamentos = [
            ("Acetaminofén", "Analgésico", 500.0),
            ("Ibuprofeno", "Antiinflamatorio", 400.0),
            ("Amoxicilina", "Antibiótico", 500.0),
            ("Loratadina", "Antihistamínico", 10.0),
            ("Omeprazol", "Gastroprotector", 20.0),
        ]
        for nombre, tipo, gramos in datos_medicamentos:
            medicamentos[nombre], _ = Medicamento.objects.get_or_create(
                nombre=nombre,
                defaults={"tipo": tipo, "gramos": gramos},
            )

        sedes = {}
        datos_sedes = [
            ("Sede Centro", "Calle 10 # 5-25"),
            ("Sede Norte", "Avenida 15 # 120-40"),
            ("Sede Sur", "Carrera 8 # 22-10"),
        ]
        for nombre, direccion in datos_sedes:
            sedes[nombre], _ = Sede.objects.get_or_create(
                nombre=nombre,
                defaults={"direccion": direccion},
            )

        inventario = [
            ("Sede Centro", "Acetaminofén", 120),
            ("Sede Centro", "Ibuprofeno", 85),
            ("Sede Norte", "Amoxicilina", 60),
            ("Sede Norte", "Loratadina", 140),
            ("Sede Sur", "Omeprazol", 95),
        ]
        for sede_nombre, medicamento_nombre, cajas in inventario:
            Almacen.objects.get_or_create(
                sede=sedes[sede_nombre],
                medicamento=medicamentos[medicamento_nombre],
                defaults={"cajas": cajas},
            )

        if Receta.objects.exists():
            print("Las recetas de prueba ya existen; no se duplican.")
        else:
            receta_1 = Receta.objects.create(
                medico=medicos["Dra. Laura Gómez"],
                paciente=pacientes["Juan Pérez"],
                fecha=date.today(),
            )
            RecetaMedicamento.objects.bulk_create(
                [
                    RecetaMedicamento(
                        receta=receta_1,
                        medicamento=medicamentos["Acetaminofén"],
                        cantidad=10,
                    ),
                    RecetaMedicamento(
                        receta=receta_1,
                        medicamento=medicamentos["Ibuprofeno"],
                        cantidad=6,
                    ),
                    RecetaMedicamento(
                        receta=receta_1,
                        medicamento=medicamentos["Omeprazol"],
                        cantidad=7,
                    ),
                ]
            )

            receta_2 = Receta.objects.create(
                medico=medicos["Dr. Carlos Ramírez"],
                paciente=pacientes["María Rodríguez"],
                fecha=date.today(),
            )
            RecetaMedicamento.objects.bulk_create(
                [
                    RecetaMedicamento(
                        receta=receta_2,
                        medicamento=medicamentos["Amoxicilina"],
                        cantidad=12,
                    ),
                    RecetaMedicamento(
                        receta=receta_2,
                        medicamento=medicamentos["Loratadina"],
                        cantidad=8,
                    ),
                ]
            )
            print(f"Recetas de prueba creadas: #{receta_1.pk} y #{receta_2.pk}")

    print(
        "Datos de prueba listos: "
        f"{Medico.objects.count()} médicos, "
        f"{Paciente.objects.count()} pacientes, "
        f"{Medicamento.objects.count()} medicamentos, "
        f"{Sede.objects.count()} sedes, "
        f"{Receta.objects.count()} recetas."
    )


def iniciar_servidor() -> None:
    print("=" * 64)
    print(" Farma · servidor de desarrollo")
    print(" Admin:   http://127.0.0.1:8000/admin/   (admin / admin123)")
    print(" API:     http://127.0.0.1:8000/api/")
    print(" Fórmula: http://127.0.0.1:8000/receta/1/")
    print("=" * 64)
    try:
        subprocess.run(
            [sys.executable, str(BASE_DIR / "manage.py"), "runserver", "127.0.0.1:8000"],
            cwd=BASE_DIR,
            check=False,
        )
    except KeyboardInterrupt:
        print("\nServidor detenido.")


def main() -> None:
    os.chdir(BASE_DIR)
    _preparar_entorno()
    aplicar_migraciones()
    crear_superusuario()
    cargar_datos_prueba()
    iniciar_servidor()


if __name__ == "__main__":
    main()
