from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
env = environ.Env()
env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = ["*"]

# URL prefix
BASE_URL = env.str("BASE_URL", "")
API_PREFIX = env.str("API_PREFIX", "api/")

HOST = env.str("HOST", "http://localhost/")

AUTH_USER_MODEL = "users.User"

# Application definition

# Django-specific apps
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# External apps
THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "djoser",
    "django_filters",
    "tinymce",
    "constance",
]

# Internal apps
INTERNAL_APPS = [
    "users",
    "rooms",
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *INTERNAL_APPS]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "django_core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:1337",
    "http://127.0.0.1:1337",
]

# CORS headers
# https://pypi.org/project/django-cors-headers/

CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]

CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

# DRF settings
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",  # noqa: E501
    "PAGE_SIZE": 10,
}


# Internationalization

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Connection max age

CONN_MAX_AGE = None

# Static files (CSS, JavaScript, Images)

STATIC_URL = f"/{BASE_URL}static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = f"/{BASE_URL}media/"
MEDIA_ROOT = BASE_DIR / "media"


# Djoser
# https://djoser.readthedocs.io/en/latest/settings.html

DJOSER = {
    "TOKEN_MODEL": None,  # We use only JWT
    "HIDE_USERS": False,
}


# DRF Spectacular
# https://drf-spectacular.readthedocs.io/en/latest/readme.html

SPECTACULAR_SETTINGS = {
    "TITLE": "REST API",
    "DESCRIPTION": "REST API",
    "VERSION": "0.0.1",
    "COMPONENT_SPLIT_REQUEST": True,
}

# Constance
# https://django-constance.readthedocs.io/en/latest/

CONSTANCE_BACKEND = "constance.backends.redisd.CachingRedisBackend"

CONSTANCE_REDIS_CACHE_TIMEOUT = 60 * 5

CONSTANCE_CONFIG = {
    "EXAMPLE_SETTING": ("Settings example", "Settings example heading", str)
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Example of group settings": ("EXAMPLE_SETTING",)
}

if env.bool("LOG_DB_QUERIES", False):
    LOGGING = {
        "version": 1,
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
                "handlers": ["console"],
            }
        },
    }
