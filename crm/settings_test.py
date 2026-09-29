"""Настройки для автоматических тестов: SQLite в памяти и быстрые хеши паролей."""

# pylint: disable=wildcard-import,unused-wildcard-import
from .settings import *  # noqa: F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
