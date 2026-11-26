# Farma

Proyecto académico de gestión de fórmulas médicas con **Django**, **Django REST
Framework** y **SQLite**.

## Requisitos

- Python 3.12 o superior
- pip

## Puesta en marcha

```bash
cd /home/jemv/Documentos/Py/Farma
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python iniciar.py
```

`iniciar.py` aplica migraciones, crea el superusuario, carga datos de prueba y
levanta el servidor en <http://127.0.0.1:8000/>.

También se puede arrancar de forma manual:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Accesos

| Recurso | URL |
| --- | --- |
| Admin | <http://127.0.0.1:8000/admin/> |
| API (navegable) | <http://127.0.0.1:8000/api/> |
| Fórmula con QR | <http://127.0.0.1:8000/receta/1/> |

Credenciales del superusuario creado por el script: **admin / admin123**.

## API REST

| Endpoint | Descripción |
| --- | --- |
| `/api/medicos/` | CRUD de médicos |
| `/api/pacientes/` | CRUD de pacientes |
| `/api/medicamentos/` | CRUD de medicamentos |
| `/api/sedes/` | CRUD de sedes |
| `/api/recetas/` | CRUD de recetas con medicamentos anidados |
| `/api/receta-medicamentos/` | CRUD de la relación receta–medicamento |
| `/api/almacen/` | CRUD del inventario por sede |

Ejemplo de respuesta de `/api/recetas/`:

```json
{
  "id": 1,
  "medico": 1,
  "medico_nombre": "Dra. Laura Gómez",
  "paciente": 1,
  "paciente_nombre": "Juan Pérez",
  "fecha": "2026-11-25",
  "medicamentos": [
    {
      "id": 1,
      "medicamento": 1,
      "nombre": "Acetaminofén",
      "tipo": "Analgésico",
      "gramos": 500.0,
      "cantidad": 10
    }
  ]
}
```

## Código QR

El QR se genera con `qrcode` en `farmacia/views.py` y se envía al template como
Base64. Su contenido es **solo** `str(receta.id)`: sin URL, sin prefijo y sin
texto adicional. La imagen se muestra en el HTML con
`data:image/png;base64,...`.

## Estructura

```text
Farma/
├── manage.py
├── iniciar.py
├── objetivos.txt
├── requirements.txt
├── README.md
├── db.sqlite3                  # se crea al migrar
├── farma/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── farmacia/
    ├── __init__.py
    ├── apps.py
    ├── admin.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── templates/
        └── farmacia/
            └── receta_formula.html
```

## Notas

- `DEFAULT_AUTO_FIELD = AutoField` para que las PK sean `INTEGER` y coincidan
  con el esquema SQL entregado.
- `RECETA.fecha` usa un `DateField` cuya columna en SQLite es `TEXT`, tal como
  define el esquema, conservando el comportamiento de fecha en admin y API.
- `CORS_ALLOW_ALL_ORIGINS = True` permite consumir la API desde cualquier
  frontend local.
- La configuración es solo para desarrollo: `DEBUG=True`, `SECRET_KEY` de
  ejemplo y API sin autenticación.
