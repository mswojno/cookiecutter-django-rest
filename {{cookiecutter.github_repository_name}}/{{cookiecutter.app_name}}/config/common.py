import os
from os.path import join

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',


        # Third party apps
        'rest_framework',            # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_rq',                 # asynchronous queuing
        'push_notifications',        # push notifications
        'versatileimagefield',       # image manipulation

        # Your apps
        'authentication',
        'users'

    )

    # https://docs.djangoproject.com/en/1.8/topics/http/middleware/
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    SECRET_KEY = 'Not a secret'
    WSGI_APPLICATION = 'wsgi.application'

    # Allow for less strict handling of urls
    APPEND_SLASH = values.BooleanValue(True)

    # Migrations
    MIGRATION_MODULES = {
        'sites': 'contrib.sites.migrations'
    }

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = DEBUG

    # Email
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')

    MANAGERS = (
        ("Author", '{{cookiecutter.email}}'),
    )

    # Postgres
    DATABASES = values.DatabaseURLValue('postgres://localhost/{{cookiecutter.app_name}}')

    # General
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    SITE_ID = 1
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static Files
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    MEDIA_URL = '/media/'

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            "rq_console": {
                "format": "%(asctime)s %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            "rq_console": {
                "level": "DEBUG",
                "class": "rq.utils.ColorizingStreamHandler",
                "formatter": "rq_console",
                "exclude": ["%(asctime)s"],
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            },
            "rq.worker": {
                "handlers": ["rq_console"],
                "level": "DEBUG"
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'PAGINATE_BY': 30,
        'PAGINATE_BY_PARAM': 'per_page',
        'MAX_PAGINATE_BY': 1000,
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    # Push notifications
    DJANGO_PUSH_NOTIFICATIONS = {
        'SERVICE': 'push_notifications.services.zeropush.ZeroPushService',
        'AUTH_TOKEN': values.Value(environ_name='ZEROPUSH_AUTH_TOKEN', environ_prefix=None)
    }

    # Versatile Image Field
    VERSATILEIMAGEFIELD_SETTINGS = {
        # The amount of time, in seconds, that references to created images
        # should be stored in the cache. Defaults to `2592000` (30 days)
        'cache_length': 2592000,
        # The name of the cache you'd like `django-versatileimagefield` to use.
        # Defaults to 'versatileimagefield_cache'. If no cache exists with the name
        # provided, the 'default' cache will be used instead.
        'cache_name': 'versatileimagefield_cache',
        # The save quality of modified JPEG images. More info here:
        # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#jpeg
        # Defaults to 70
        'jpeg_resize_quality': 70,
        # The name of the top-level folder within storage classes to save all
        # sized images. Defaults to '__sized__'
        'sized_directory_name': '__sized__',
        # The name of the directory to save all filtered images within.
        # Defaults to '__filtered__':
        'filtered_directory_name': '__filtered__',
        # The name of the directory to save placeholder images within.
        # Defaults to '__placeholder__':
        'placeholder_directory_name': '__placeholder__',
        # Whether or not to create new images on-the-fly. Set this to `False` for
        # speedy performance but don't forget to 'pre-warm' to ensure they're
        # created and available at the appropriate URL.
        'create_images_on_demand': False
    }
