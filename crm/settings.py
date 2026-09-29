"""
Настройки Django-проекта CRM-системы.

По требованиям технического задания в качестве СУБД используется
PostgreSQL. Для удобства локальной разработки/проверки без
предварительной настройки PostgreSQL предусмотрен временный переход
на SQLite через переменную окружения DJANGO_USE_SQLITE=1
(см. README.md).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    """Прочитать булево значение переменной окружения."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# ЗАМЕНИТЕ этот ключ на собственный перед выкладкой проекта в продакшен.
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-crm-demo-secret-key-change-me",
)

DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Приложения CRM-системы
    "users.apps.UsersConfig",
    "products.apps.ProductsConfig",
    "advertisements.apps.AdvertisementsConfig",
    "leads.apps.LeadsConfig",
    "contracts.apps.ContractsConfig",
    "customers.apps.CustomersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crm.wsgi.application"
ASGI_APPLICATION = "crm.asgi.application"

# --- База данных -----------------------------------------------------------
if env_bool("DJANGO_USE_SQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DJANGO_DB_NAME", "crm"),
            "USER": os.getenv("DJANGO_DB_USER", "crm_user"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", "crm_password"),
            "HOST": os.getenv("DJANGO_DB_HOST", "localhost"),
            "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
        }
    }

# --- Валидация паролей -------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Локализация -------------------------------------------------------------
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# --- Статика и медиафайлы -----------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Фикстуры с тестовыми данными --------------------------------------------
# Позволяет запускать `python manage.py loaddata demo_data.json`,
# не указывая полный путь до файла (см. README.md, раздел
# «Загрузка тестовых данных»).
FIXTURE_DIRS = [BASE_DIR / "fixtures"]

# --- Аутентификация -----------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "login"
