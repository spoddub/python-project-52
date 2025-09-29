from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

from task_manager.config import Config

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

BASE_DIR = Path(__file__).resolve().parent.parent

config = Config()

SECRET_KEY = config.secret_key
DEBUG = not config.is_production
ALLOWED_HOSTS = config.allowed_hosts
CSRF_TRUSTED_ORIGINS = getattr(config, "csrf_trusted_origins", [])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "task_manager",
    "task_manager.apps.core",
    "task_manager.apps.users",
    "task_manager.apps.statuses",
    "task_manager.apps.tasks",
    "task_manager.apps.labels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "task_manager.apps.core.middleware.LoginRequiredWithMessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "task_manager.apps.core.middleware.RollbarNotifierMiddleware",
]


ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "task_manager" / "templates"],
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

WSGI_APPLICATION = "task_manager.wsgi.application"

DATABASES = {"default": config.setup_database(BASE_DIR)}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 3},
    }
]

AUTH_USER_MODEL = "users.User"
LOGIN_URL = reverse_lazy("login")


LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "task_manager" / "apps_static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOCALE_PATHS = [BASE_DIR / "locale"]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

ROLLBAR = {
    "access_token": config.rollbar_token,
    "environment": "development" if DEBUG else "production",
    "code_version": "1.0",
    "root": BASE_DIR,
}
