# https://docs.djangoproject.com/en/1.10/ref/settings/

import os

from decouple import config  # noqa

import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

'''
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": base_dir_join("db.sqlite3"),}
}

import dj_database_url

DATABASES = {

'default': {

'URI':'postgres://jgynaanmwihthi:3e82cbd904e35b9d55b5bb34d31157614dcfabd7e8d9b27ed6494c79791fd0c8@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d5pcf5p4nnug5f',

'NAME': 'd5pcf5p4nnug5f',

'USER': 'jgynaanmwihthi',

'PASSWORD': '3e82cbd904e35b9d55b5bb34d31157614dcfabd7e8d9b27ed6494c79791fd0c8',

'HOST': '[ec2-54-164-22-242.compute-1.amazonaws.com](http://ec2-54-164-22-242.compute-1.amazonaws.com/)',

'PORT': '5432', # 8000 is default

},
}'''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def base_dir_join(*args):
    return os.path.join(BASE_DIR, *args)


SITE_ID = 1

SECURE_HSTS_PRELOAD = True

DEBUG = True

ADMINS = (("Deborah", "deborah.mendonca@vinta.com.br"),)

AUTH_USER_MODEL = "users.User"
STATUS_MODEL = "sequence.Status"

POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"



ALLOWED_HOSTS = []

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_js_reverse",
    "webpack_loader",
    "import_export",
    "common",
    "users",
    "battle",
    "pokemon",
    'templated_email',
    'dal_select2',
    'dal',
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pokebattle.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir_join("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.sentry_dsn",
                "common.context_processors.commit_sha",
            ],
        },
    },
]

WSGI_APPLICATION = "pokebattle.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (base_dir_join("../frontend"),)

# Webpack
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,  # on DEBUG should be False
        "STATS_FILE": base_dir_join("../webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [".+\.hot-update.js", ".+\.map"],
    }
}

# Celery
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACKS_LATE = True
CELERY_TIMEZONE = TIME_ZONE

# Sentry
SENTRY_DSN = config("SENTRY_DSN", default="")
COMMIT_SHA = config("HEROKU_SLUG_COMMIT", default="")

'''
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

FROM_EMAIL = config('FROM_EMAIL', default='deborah.mendonca@vinta.com.br')

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'
