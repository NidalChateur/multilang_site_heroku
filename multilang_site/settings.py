"""
Django settings for multilang_site project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import django_heroku
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .utils.create_env import create_environment_variables_file

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


if DEBUG:
    create_environment_variables_file()

    # load file ".env"
    load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY")
FERNET_KEY = os.environ.get("FERNET_KEY")
JWT_PASSWORD = os.environ.get("JWT_PASSWORD").encode("utf-8")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


ALLOWED_HOSTS = []


# Application definition
INTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTENSION_APPS = ["django_bootstrap5", "rest_framework"]

CREATED_APPS = ["authentication", "main", "api", "chatbot", "error"]

INSTALLED_APPS = INTERNAL_APPS + EXTENSION_APPS + CREATED_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    #
    "django.contrib.sessions.middleware.SessionMiddleware",
    # used by i18n
    "django.middleware.locale.LocaleMiddleware",
    #
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "multilang_site.urls"

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

WSGI_APPLICATION = "multilang_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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


# Internationalization (i18n)
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# translation path
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# languages list
LANGUAGES = [
    ("fr", _("French")),
    ("en", _("English")),
]

# default language
LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication :

# Path added to user model
AUTH_USER_MODEL = "authentication.User"

# redirect user that have to login
LOGIN_URL = "login"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# whitenoise config :
# # Following settings only make sense on production and may break development environments.
if not DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = BASE_DIR / "staticfiles"

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# heroku config (deployment)
django_heroku.settings(locals())
