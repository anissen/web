# encoding: utf8
"""
Django settings for tkweb project.
"""

from __future__ import absolute_import, unicode_literals, division

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'bootstrap3',
    'constance',
    'constance.backends.database',
    'jfu',
    'sorl.thumbnail',
    'versatileimagefield',
    'django_cleanup',
    'macros',
]

LOCAL_APPS = [
    'tkweb.apps.calendar',
    'tkweb.apps.gallery',
    'tkweb.apps.jubi',
    'tkweb.apps.redirect',
    'tkweb.apps.tkbrand',
    'idm',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Internationalization
# --------------------
# https://docs.djangoproject.com/en/1.8/topics/i18n/

TIME_ZONE = 'Europe/Copenhagen'
LANGUAGE_CODE = 'da'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# URLs
# ----

ROOT_URLCONF = 'tkweb.urls'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

LOGIN_URL = '/admin/login'

# Media files
# -----------

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')


# Static files
# ------------

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Don't forget to use absolute paths, not relative paths.
    "static-src",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Bootstrap3
# ----------

BOOTSTRAP3 = {
    # The base_url is the default from django-bootstrap3. It is included here
    # so the version can follow the version of the git-submodule of bootstrap
    # located at static-src/bootstrap.

    # The javascript is loaded based on the base_url. Currently from a CDN.
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/',

    # The css is from static-src/bootstrap via static-src/style.less.
    # This way it is possible to customize the css\less, without all the
    # dependencies need to compile the whole bootstrap.
    #
    # This file can be updated with
    # `lessc --clean-css style.less style.min.css` on a machine with `node.js`,
    # `less` and `less-plugin-clean-css`.
    'css_url': STATIC_URL + 'style.min.css',
}

# Templates
# ---------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
            'debug': False,
        },
    },
]

# Thumbnails
# ----------

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'gallery': [
        ('gallery_253', 'crop__253x253'),
        ('image_400', 'thumbnail__400x400'),
        ('image_720', 'thumbnail__720x720'),
        ('image_940', 'thumbnail__940x940'),
        ('image_1140', 'thumbnail__1140x1140'),
        ('image_2280', 'thumbnail__2280x2280'),
    ],
}

# Middleware
# ----------

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Test
# ----

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Sites
# -----
SITE_ID = 1


# Constance
# ---------
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'GFYEAR': (2015,
               'Året hvor nuværende BEST blev valgt'),
    'ICAL_URL': ('https://www.google.com/calendar/ical/best@taagekammeret.dk/public/basic.ics',
                 'iCalendar URLen hvor den offentlige kalender bliver genereret fra.'),
    'CAL_URL': ('//calendar.google.com/calendar/embed?src=BEST@TAAGEKAMMERET.dk&ctz=Europe/Copenhagen',
                'URLen til \'Tilføj til din egen kalender\'-linket på kalendersiden.'),
}
