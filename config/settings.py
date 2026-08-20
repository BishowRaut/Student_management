"""
Django settings for config project.

Student Management System
"""

import os
from pathlib import Path


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-only-change-this-key",
)

DEBUG = os.environ.get(
    "DEBUG",
    "False",
).lower() == "true"


# =========================================================
# VERCEL / CUSTOM DOMAIN
# =========================================================

VERCEL_URL = os.environ.get("VERCEL_URL")
CUSTOM_DOMAIN = os.environ.get("CUSTOM_DOMAIN")


# =========================================================
# ALLOWED HOSTS
# =========================================================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]

# Add Vercel deployment hostname
if VERCEL_URL:
    VERCEL_HOST = (
        VERCEL_URL
        .replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
    )

    if VERCEL_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(VERCEL_HOST)


# Add custom domain
if CUSTOM_DOMAIN:
    CUSTOM_HOST = (
        CUSTOM_DOMAIN
        .replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
    )

    if CUSTOM_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(CUSTOM_HOST)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Student Management System
    "studentapp",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# DATABASE
# =========================================================
#
# LOCAL:
#     SQLite
#
# VERCEL:
#     PostgreSQL using DATABASE_URL
#
# =========================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


if VERCEL_URL:
    # -----------------------------------------------------
    # PRODUCTION: VERCEL
    # -----------------------------------------------------

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not configured in Vercel Environment Variables."
        )

    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:
    # -----------------------------------------------------
    # LOCAL DEVELOPMENT
    # -----------------------------------------------------

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

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


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================================================
# AUTHENTICATION
# =========================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================

CSRF_TRUSTED_ORIGINS = [
    "https://student-management-three-alpha.vercel.app",
]

# Add Vercel deployment URL
if VERCEL_URL:

    VERCEL_ORIGIN = VERCEL_URL

    if not (
        VERCEL_ORIGIN.startswith("http://")
        or VERCEL_ORIGIN.startswith("https://")
    ):
        VERCEL_ORIGIN = f"https://{VERCEL_ORIGIN}"

    VERCEL_ORIGIN = VERCEL_ORIGIN.rstrip("/")

    if VERCEL_ORIGIN not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(
            VERCEL_ORIGIN
        )


# Add custom domain
if CUSTOM_DOMAIN:

    CUSTOM_ORIGIN = CUSTOM_DOMAIN

    if not (
        CUSTOM_ORIGIN.startswith("http://")
        or CUSTOM_ORIGIN.startswith("https://")
    ):
        CUSTOM_ORIGIN = f"https://{CUSTOM_ORIGIN}"

    CUSTOM_ORIGIN = CUSTOM_ORIGIN.rstrip("/")

    if CUSTOM_ORIGIN not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(
            CUSTOM_ORIGIN
        )


# =========================================================
# PRODUCTION SECURITY
# =========================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"