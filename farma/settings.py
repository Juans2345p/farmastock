"""
Configuración de Django para el proyecto académico Farma.

Entorno de desarrollo local con SQLite. No usar esta configuración tal cual
en producción (SECRET_KEY expuesta, DEBUG activo y CORS completamente abierto).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Clave solo para desarrollo académico local.
SECRET_KEY = "django-insecure-farma-academico-2026-cambiar-en-produccion"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# URL base pública que se codifica dentro del QR de cada receta.
# Ejemplos:
#   FARMA_PUBLIC_URL=http://192.168.1.50:8000
#   FARMA_PUBLIC_URL=https://farmacia.midominio.com
# Si se deja vacía, se usa el host con el que se abrió la página
# (localhost, IP de la LAN, dominio, etc.).
FARMA_PUBLIC_URL = os.environ.get("FARMA_PUBLIC_URL", "").strip().rstrip("/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "corsheaders",
    "rest_framework",
    # Aplicación del proyecto
    "farmacia",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # CorsMiddleware debe ir lo más arriba posible, antes de CommonMiddleware.
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "farma.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "farma.wsgi.application"
ASGI_APPLICATION = "farma.asgi.application"

# Base de datos local: un único archivo SQLite en la raíz del proyecto.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Proyecto académico: sin reglas de contraseña para facilitar las pruebas.
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

# AutoField (INTEGER) para que las PK coincidan exactamente con el esquema SQL
# entregado (Django 6 usaría BigAutoField por defecto).
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# API abierta para cualquier frontend local (React, Vue, Angular, etc.).
CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}
