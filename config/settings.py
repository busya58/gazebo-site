"""
Django settings for config project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные из файла .env
load_dotenv(BASE_DIR / ".env")


# Security

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in {
    "true",
    "1",
    "yes",
    "on",
}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core.apps.CoreConfig",
    "pages.apps.PagesConfig",
    "cabinet",
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

ROOT_URLCONF = "config.urls"

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
                "core.context_processors.site_data",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Internationalization

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"

USE_I18N = True
USE_TZ = True


# Static files

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# Uploaded media files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Email

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}


# Site data

SITE_NAME = "Беседки и Вольеры РФ"
SITE_SLOGAN = "Беседки, вольеры и навесы по всей России"

SITE_PHONE = "+7 (925) 055-98-88"
SITE_PHONE_HREF = "+79250559888"
SITE_EMAIL = "hh8754905@gmail.com"
SITE_ADDRESS = "г. Москва и Московская область"
SITE_GEOGRAPHY = "Вся Россия"

# Перед публикацией замените на настоящий домен
SITE_URL = "https://example.ru"

SITE_DESCRIPTION = (
    "Изготовление и установка беседок, вольеров, навесов "
    "и других конструкций на заказ по всей России."
)


# Authentication

LOGIN_URL = "cabinet:login"
LOGIN_REDIRECT_URL = "cabinet:dashboard"
LOGOUT_REDIRECT_URL = "cabinet:login"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"