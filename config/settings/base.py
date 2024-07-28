"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import ast
import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=f"{BASE_DIR.parent}/.env")

# URL to use when referring to media files located in MEDIA_ROOT
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory where user-uploaded files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Logging definition

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console_handler"],
        },
        "django.request": {
            "handlers": ["error_file_handler", "console_handler", "mail_admins"],
            "propagate": False,
        },
        "django.server": {
            "handlers": ["access_file_handler", "console_handler"],
            "propagate": False,
        },
    },
    "handlers": {
        "console_handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "error_formatter",
            "stream": "ext://sys.stdout",
        },
        "error_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "error_formatter",
            "level": "WARNING",
            "filename": f"{BASE_DIR}/error.log",
            "when": "D",
            "interval": 30,
            "backupCount": 1,
        },
        "access_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "access_formatter",
            "level": "INFO",
            "filename": f"{BASE_DIR}/access.log",
            "when": "D",
            "interval": 30,
            "backupCount": 1,
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "formatters": {
        "access_formatter": {"format": "%(message)s"},
        "error_formatter": {
            "()": "core.log.RequestFormatter",
            "format": "--- Logging %(levelname)s at %(asctime)s --- \n%(message)s\n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue"  # log while DEBUG=True
        }
    },
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party libraries
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "storages",
    # local apps
    "app.single.apps.SingleConfig",
    "app.bulk.apps.BulkConfig",
    "app.account.apps.AccountConfig",
    "app.template.apps.TemplateConfig",
    "app.delivery.apps.DeliveryConfig",
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

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exceptions.app_exception_handler.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "core.utils.JWTAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Email Service Application",
    "DESCRIPTION": "Backend Application That Integrates With A Mail Server For Sending Emails",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {
        "name": "Michael Asumadu",
        "email": "michaelasumadu10@gmail.com",
    },
    "LICENSE": {"name": "MIT"},
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("OBJECT_STORAGE_ACCESS_KEY"),
            "secret_key": env("OBJECT_STORAGE_SECRET_KEY"),
            "bucket_name": env("OBJECT_STORAGE_BUCKET"),
            "endpoint_url": env("OBJECT_STORAGE_URL"),
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TEST": {
            "NAME": env("TEST_DB_NAME"),
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
SERVER_EMAIL = env("SERVER_EMAIL")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
ADMINS = [ast.literal_eval(admin) for admin in env("ADMINS").split("|")]
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS").lower() in ("true", "1", "t")
EMAIL_USE_SSL = env("EMAIL_USE_SSL").lower() in ("true", "1", "t")

# Celery Settings
CELERY_BROKER_URL = (
    f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_SERVER')}:{env('REDIS_PORT')}"
)
CELERY_RESULT_BACKEND = (
    f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_SERVER')}:{env('REDIS_PORT')}"
)

# Jwt Settings
JWT_ALGORITHMS = ["HS256", "RS256"]

# Keycloak Settings
KEYCLOAK_URI = ""
KEYCLOAK_REALM = ""
