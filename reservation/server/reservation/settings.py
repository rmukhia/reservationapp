"""
Django settings for reservation project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/

For security reasons, please deploy only *.pyc file
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Client dir 

CLIENT_DIR = os.path.join(os.path.dirname(BASE_DIR), 'client')

ANGULARJS_DIR = os.path.join(CLIENT_DIR, "public")
MEDIA_DIR = os.path.join(os.path.dirname(BASE_DIR),"media")

# Mail Pre-requisite

EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


EMAIL_HOST_USER = 'qaautomation@ixiacom.com'
EMAIL_SEND_AS_USER = 'noreply-appsecin-lab-reservation@ixiacom.com'
EMAIL_HOST_PASSWORD = r"48a7IXt%jJ*Q4d4ETN3l" 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vtz^l%z+3u4z+t7q&rjw_78^(tj!k2v&c(+1@hi_ywp@bf7bop'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'resources.apps.ResourcesConfig',
    'records.apps.RecordsConfig',
    'rest_framework',
    'djangobower',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reservation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(CLIENT_DIR, 'django_templates')],
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


WSGI_APPLICATION = 'reservation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
 }

#DATABASES = {
#  'default': {
#       'ENGINE': 'django.db.backends.mysql',
#        'OPTIONS': {
#          'read_default_file': os.path.join(os.path.dirname(BASE_DIR), 'mysql-debug.conf'),
#      },
#   }
#}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
     # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
     # 'PAGE_SIZE':100,
}

STATICFILES_DIRS = [
    ANGULARJS_DIR,
]

MEDIAFILES_DIRS = [
    MEDIA_DIR,
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'djangobower.finders.BowerFinder'
]

BOWER_COMPONENTS_ROOT = os.path.join(CLIENT_DIR, 'components')

BOWER_PATH = '/usr/bin/bower'

BOWER_INSTALLED_APPS = (
    'underscore#1.8.2',
    'angularjs#1.5.3',
    'angular-ui-router#0.2.18',
    'angular-bootstrap#1.3.1',
    'bootstrap#3.3.6',
    'ng-file-upload#12.0.4',
    'angular-animate#1.5.3'
)

REST_API_URL_BASE = 'rest'

CLIENT_APP_CONFIG = {
    'rest_api_base': REST_API_URL_BASE,
    'title': 'Reservation', 
    'app_name': 'reservation', 
    'welcome': 'Welcome', 
    'welcome_description': 'To start reserving Sign In.',
    'welcome_button_text': 'Sign In',
    'hostname': 'http://localhost:9000'
}

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static');
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media');
