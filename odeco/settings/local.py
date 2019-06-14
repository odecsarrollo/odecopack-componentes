"""Development settings and globals."""

from __future__ import absolute_import

import os

from .base import *

############### SECRET FILE
import json

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception. from django.core.exceptions import ImproperlyConfigured
# JSON-based secrets module
from django.core.exceptions import ImproperlyConfigured

with open("secretsLocal.json") as f:
    secrets = json.loads(f.read())


def get_secret(setting, variable, secrets=secrets):
    """ Get the environment setting or return exception """
    try:
        return secrets[setting][variable]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


############### END SECRET FILE

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Admin', 'correo@correo.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"{{ secret_key }}"
########## END SECRET CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

THIRD_PART_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS = INSTALLED_APPS + THIRD_PART_APPS

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
######### END CACHE CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Prueba cambios

DATABASES = {
    'default': {
        'ENGINE': get_secret("DATABASE_LOCAL", "ENGINE"),
        'NAME': get_secret("DATABASE_LOCAL", "NAME"),
        'USER': get_secret("DATABASE_LOCAL", "USER"),
        'PASSWORD': get_secret("DATABASE_LOCAL", "PASSWORD"),
        'HOST': get_secret("DATABASE_LOCAL", "HOST"),
        'PORT': get_secret("DATABASE_LOCAL", "PORT"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
########## END DATABASE CONFIGURATION

########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

# 'EMAIL_IS_LOCAL'
if str_to_bool(get_secret("EMAIL_SERVER", "EMAIL_IS_LOCAL")):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = get_secret("EMAIL_SERVER", "EMAIL_HOST")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_secret("EMAIL_SERVER", "EMAIL_HOST_PASSWORD")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_secret("EMAIL_SERVER", "EMAIL_HOST_USER")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = get_secret("EMAIL_SERVER", "EMAIL_PORT")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = str_to_bool(get_secret("EMAIL_SERVER", "EMAIL_USE_TLS"))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'desarrollo.odecopack@gmail.com'

EMAIL_USE_SSL = str_to_bool(get_secret("EMAIL_SERVER", "EMAIL_USE_SSL"))

DEFAULT_FROM_EMAIL = get_secret("EMAIL_SERVER", "DEFAULT_FROM_EMAIL")

########## END EMAIL CONFIGURATION


########## DEBUG TOOLBAR CONFIGURATION CONFIGURATION
INTERNAL_IPS = '127.0.0.1'
########## END TOOLBAR CONFIGURATION CONFIGURATION
