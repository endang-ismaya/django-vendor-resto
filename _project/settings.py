import os
import dotenv
from pathlib import Path
from django.utils.log import DEFAULT_LOGGING
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# environment
dotenv.read_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # internal
    "_apps.account",
    "_apps.vendor",
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

ROOT_URLCONF = "_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}

AUTH_USER_MODEL = "account.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "_project/static")]

# MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING
LOGLEVEL = os.environ.get("LOGLEVEL", "info").upper()
LOGGING = {
    "version": 1,
    # The version number of our log
    "disable_existing_loggers": False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    "handlers": {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARNING",
            # "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug_logs/dailylog.log",
            "formatter": "default",
            "when": "d",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf8",
        },
        "file_info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            # "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug_logs/dailylog.log",
            "formatter": "default",
            "when": "d",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "formatters": {
        "default": {
            # exact format is not important, this is the minimum information
            # "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    "loggers": {
        # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        "": {
            "handlers": [
                "file",
                "console",
            ],  # notice how file variable is called in handler which has been defined above
            "level": "WARNING",
            "propagate": True,
        },
        # Our application code
        "app": {
            "level": LOGLEVEL,
            "handlers": ["console", "file_info"],
            # Avoid double logging because of root logger
            "propagate": False,
        },
    },
}


# MESSAGES
MESSAGE_TAGS = {messages.ERROR: "danger", messages.SUCCESS: "success"}

# EMAIL CONFIGURATION
# SMTP Configuration
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


# Password reset
PASSWORD_RESET_TIMEOUT_DAYS = 1
