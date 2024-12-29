from pathlib import Path
import environ

from . import __version__


# █▀▀ █▄░█ █░█ ▀
# ██▄ █░▀█ ▀▄▀ ▄
# -- -- -- -- --
env = environ.Env(
    # set casting, default value
    VERSION=(str, __version__),
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'j9QGbvM9Z4otb47'),
    TZ=(str, 'UTC')
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env((BASE_DIR / '.env'))


# █▀▀ █▀█ █▀█ █▀▀ ▀
# █▄▄ █▄█ █▀▄ ██▄ ▄
# -- -- -- -- -- -
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

VERSION = env('VERSION')

# SECURITY WARNING: keep the secret key used in production secret!
# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# False if not in os.environ because of casting above env var
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["*"])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'answers.apps.AnswersConfig',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moodlehack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'moodlehack.wsgi.application'


# █▀▄ ▄▀█ ▀█▀ ▄▀█ █▄▄ ▄▀█ █▀ █▀▀ ▀
# █▄▀ █▀█ ░█░ █▀█ █▄█ █▀█ ▄█ ██▄ ▄
# -- -- -- -- -- -- -- -- -- -- --
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': env.db_url(
        'SQLITE_URL',
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa:E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'  # 'en-us'

TIME_ZONE = env('TZ')

USE_I18N = True
USE_L10N = True

USE_TZ = True


# █▀ ▀█▀ ▄▀█ ▀█▀ █ █▀▀ ▀
# ▄█ ░█░ █▀█ ░█░ █ █▄▄ ▄
# -- -- -- -- -- -- -- -
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'answers' / 'static',
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# █▀▀ ▀▄▀ ▀█▀ █▀▀ █▄░█ ▀█▀ █ █▀█ █▄░█ █▀ ▀
# ██▄ █░█ ░█░ ██▄ █░▀█ ░█░ █ █▄█ █░▀█ ▄█ ▄
# -- -- -- -- -- -- -- -- -- -- -- -- -- -

# django-crispy-forms and crispy-bootstrap5
# https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django rest framework:
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

if DEBUG:
    REST_FRAMEWORK.get(
        'DEFAULT_RENDERER_CLASSES', []
    ).append('rest_framework.renderers.BrowsableAPIRenderer')
    REST_FRAMEWORK.get(
        'DEFAULT_PARSER_CLASSES', []
    ).append('rest_framework.renderers.BrowsableAPIRenderer')

# https://drf-spectacular.readthedocs.io/en/latest/readme.html
SPECTACULAR_SETTINGS = {
    'TITLE': 'AKVOLABEAN',
    'DESCRIPTION': 'Web application to collect ready-made answers.',
    'VERSION': VERSION,
    'SERVE_INCLUDE_SCHEMA': True,
    'SERVE_PUBLIC': False,
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
}
