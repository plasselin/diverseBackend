import environ
import os
from pathlib import Path
import corsheaders
from django.contrib import staticfiles
import chatapi
import custom_auth

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'http://localhost:7861/',
    'testserver',
    'http://localhost:7000/',
]

INSTALLED_APPS = [
    "custom_auth",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "django.contrib.staticfiles",
    # "diverseai.apps.DiverseaiConfig",
    "corsheaders",
    "chatapi",
]

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

ROOT_URLCONF = "djangoProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = "djangoProject.wsgi.application"

OPENAI_ORGANIZATION = env('OPENAI_ORGANIZATION')
OPENAI_API_KEY = env('OPENAI_API_KEY')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env('DB_NAME'),
        "USER": env('DB_USER'),
        "PASSWORD": env('DB_PASSWORD'),
        "HOST": env('DB_HOST'),
        "PORT": env('DB_PORT'),
    }
}



CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'HTTP',
]

CORS_ALLOWED_HEADERS = [
    '*',
]

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

DEBUG = True

AUTH_USER_MODEL = 'custom_auth.CustomUser'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LANGUAGE_CODE = "en-us"

SITE_ID = 1

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

