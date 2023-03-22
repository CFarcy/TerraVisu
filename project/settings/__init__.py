"""
Django settings for temp project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from decouple import Csv, config
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

with open(BASE_DIR / "VERSION") as version_file:
    VERSION = version_file.read().strip()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="please-override-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.gis",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_auth_oidc",
    "rest_framework",
    "rest_framework_jwt",
    "rest_framework_jwt.blacklist",
    "rest_framework_gis",
    "crispy_forms",
    "crispy_bootstrap5",
    "geostore",
    "mapbox_baselayer",
    "django_filters",
    "django_celery_results",
    "django_celery_beat",
    "constance",
    "constance.backends.database",
    "corsheaders",
    "project.accounts",
    "project.frontend",
    "project.visu",
    "project.geosource",
    "project.terra_layer",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

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
                "project.context_processors.custom_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

VAR_DIR = PROJECT_DIR / "var"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static_dj/"
STATIC_ROOT = PROJECT_DIR / "public" / "static_dj"
MEDIA_URL = "media/"
MEDIA_ROOT = PROJECT_DIR / "public" / "media"
ADMIN_ROOT = PROJECT_DIR / "public" / "admin"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
AUTH_USER_MODEL = "accounts.User"
LOCALE_PATHS = (BASE_DIR / "locales",)
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap5",)

CRISPY_TEMPLATE_PACK = "bootstrap5"

GEOSOURCE_LAYER_CALLBACK = "project.geosource.geostore_callbacks.layer_callback"
GEOSOURCE_FEATURE_CALLBACK = "project.geosource.geostore_callbacks.feature_callback"
GEOSOURCE_CLEAN_FEATURE_CALLBACK = "project.geosource.geostore_callbacks.clear_features"
GEOSOURCE_DELETE_LAYER_CALLBACK = "project.geosource.geostore_callbacks.delete_layer"

REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 100,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "project.pagination.PagePagination",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}


JWT_AUTH = {
    "JWT_PAYLOAD_HANDLER": "project.accounts.jwt_payload.terra_payload_handler",
    "JWT_EXPIRATION_DELTA": timedelta(seconds=9999),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "TerraVisu API",
    "DESCRIPTION": "API for TerraVisu application",
    "VERSION": VERSION,
    "SERVE_INCLUDE_SCHEMA": False,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f'redis://{os.getenv("REDIS_HOST", "redis")}:{os.getenv("REDIS_PORT", "6379")}',
    }
}

ES_URL = config("ES_URL", default="http://elasticsearch:9200", cast=str)

SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_FILE_PATH = VAR_DIR / "cache" / "sessions"

CONSTANCE_ADDITIONAL_FIELDS = {"image_field": ["django.forms.ImageField", {}]}

CONSTANCE_CONFIG = {
    "INSTANCE_TITLE": ("TerraVisu", _("Instance title"), str),
    "INSTANCE_CREDITS": ("Source: TerraVisu", _("Instance credits"), str),
    "INSTANCE_LOGO": ("/static_dj/img/logo.webp", _("Logo"), "image_field"),
    "INSTANCE_LOGO_FRONTEND_URL": ("/", _("Logo frontend URL"), str),
    "INSTANCE_FAVICON": ("/static_dj/img/favicon.ico", _("Favicon"), "image_field"),
    "INSTANCE_SPLASHSCREEN": (
        "/static_dj/img/splashscreen.png",
        _("Splashscreen"),
        "image_field",
    ),
    "MAPBOX_ACCESS_TOKEN": ("", "Mapbox access token", str),
    "MAP_BBOX_LNG_MIN": (-180.0, _("Map bbox lng mini"), float),
    "MAP_BBOX_LNG_MAX": (180.0, _("Map bbox lng maxi"), float),
    "MAP_BBOX_LAT_MIN": (-90.0, _("Map bbox lat mini"), float),
    "MAP_BBOX_LAT_MAX": (90.0, _("Map bbox lat maxi"), float),
    "MAP_MAX_ZOOM": (23.0, _("Map max zoom"), float),
    "MAP_MIN_ZOOM": (0.0, _("Map min zoom"), float),
    "MAP_DEFAULT_ZOOM": (7.0, _("Map default zoom"), float),
    "MAP_DEFAULT_LNG": (2.0, _("Map default lng"), float),
    "MAP_DEFAULT_LAT": (44.0, _("Map default lat"), float),
    "VIEW_ROOT_PATH": ("view", _("Frontend view root path"), str),
    "DEFAULT_VIEW_NAME": ("", _("Frontend default view name"), str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "General Options": {"fields": ("INSTANCE_TITLE",)},
    "Theme Options": {
        "fields": (
            "INSTANCE_LOGO",
            "INSTANCE_LOGO_FRONTEND_URL",
            "INSTANCE_FAVICON",
            "INSTANCE_SPLASHSCREEN",
            "INSTANCE_CREDITS",
        ),
        "collapse": True,
    },
    "Map BBOX options": {
        "fields": (
            "MAP_BBOX_LNG_MIN",
            "MAP_BBOX_LNG_MAX",
            "MAP_BBOX_LAT_MIN",
            "MAP_BBOX_LAT_MAX",
        ),
        "collapse": True,
    },
    "Map Zoom options": {
        "fields": ("MAP_MAX_ZOOM", "MAP_MIN_ZOOM"),
        "collapse": True,
    },
    "Map default options": {
        "fields": ("MAP_DEFAULT_ZOOM", "MAP_DEFAULT_LNG", "MAP_DEFAULT_LAT"),
        "collapse": True,
    },
    "Mapbox options": {
        "fields": ("MAPBOX_ACCESS_TOKEN",),
        "collapse": True,
    },
    "Frontend options": {
        "fields": ("VIEW_ROOT_PATH", "DEFAULT_VIEW_NAME"),
        "collapse": True,
    },
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_CACHE_BACKEND = "default"

CELERY_TASK_ALWAYS_EAGER = False

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", default=None)
CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN", default=None)

SSL_ENABLED = config("SSL_ENABLED", default=False, cast=bool)
if SSL_ENABLED:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# OpenID
OIDC_ENABLE_LOGIN = config("OIDC_ENABLE_LOGIN", default=False, cast=bool)
OIDC_DISABLE_INTERNAL_LOGIN = config(
    "OIDC_DISABLE_INTERNAL_LOGIN", default=False, cast=bool
)
AUTH_SERVER = config("OIDC_AUTH_SERVER", default=None)
AUTH_CLIENT_ID = config("OIDC_AUTH_CLIENT_ID", default=None)
AUTH_CLIENT_SECRET = config("OIDC_AUTH_CLIENT_SECRET", default=None)
AUTH_SCOPE = config("OIDC_AUTH_SCOPE", default="openid", cast=Csv())
AUTH_GET_USER_FUNCTION = "project.accounts.oidc:get_user"

API_SCHEMA = config("API_SCHEMA", default=False, cast=bool)
API_SWAGGER = config("API_SWAGGER", default=False, cast=bool)  # NEED API_SCHEMA
API_REDOC = config("API_REDOC", default=False, cast=bool)  # NEED API_SCHEMA

SENTRY_DSN = config("SENTRY_DSN", default="", cast=str)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
        traces_sample_rate=config("SENTRY_TRACE_SAMPLE_RATE", default=0.2, cast=float),
        send_default_pii=config("SENTRY_SEND_DEFAULT_PII", default=True, cast=bool),
        release=f"terra-visu@{VERSION}",
    )
