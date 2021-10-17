"""
Django settings for Trackem project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%r2#pc!hl*ih2l^(+ulh6c3ja!-+pbhdm%+yi4efwxwp$#4oc5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  #development only
    #edward test
ALLOWED_HOSTS = ['127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django_filters',
    'UploadExcel.apps.UploadexcelConfig',
    'crispy_forms',
    'userT.apps.UsertConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'Tenant',
    'simple_history',
    'rest_framework',
    'debug_toolbar',

    
    #'django_seed',

]
AUTH_USER_MODEL =   'userT.CustomUser'#using custom user so can put in disipline etc
USE_TZ = True #to use time zone to help with  with auto_now thatts giving a wrong time
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    
]

ROOT_URLCONF = 'Trackem.urls'

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

WSGI_APPLICATION = 'Trackem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trackemupgrade',
        'USER': 'root',
        'PASSWORD': 'Nice10day',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
  #      'NAME': str(os.path.join(BASE_DIR, "db.sqlite3")),
  #  }
#}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'main'
#LOGIN_REDIRECT_URL = 'login'


#fetch static image test
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


#CrispyForms Template --> this is to enable the form fields to stretch across the whole div
CRISPY_TEMPLATE_PACK = 'bootstrap4'
 
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
#LOGIN_REDIRECT_URL = 'Login'
#CRISPY_TEMPLATE_PACK = 'bootstrap4'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.eu-west-1.awsapps.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_HOST_USER = 'ehstools@prism-ehstools.awsapps.com'
EMAIL_HOST_PASSWORD = 'Nice10day'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'ehstools@prism-ehstools.awsapps.com' #required to be declared email globally because we are using django in-built django reset functions

#gmail email settings
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'actionstracker@gmail.com'
#EMAIL_HOST_PASSWORD = 'Helloworld2021'
#EMAIL_USE_SSL = False

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]