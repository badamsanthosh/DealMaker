"""
Django settings for dealmaker project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('SECRET_HOST')
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'secureportal.dealmax.com.au',
    'api.dealmax.com.au'
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home_loans',
    'lending',
    'meta',
    'third_party',
    'user_mgmt',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

]

ROOT_URLCONF = 'dealmaker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'dealmaker.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PWD')
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.dmx_exception_handler.custom_drf_exception',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

# Password validation
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
)

# Custom User Model
AUTH_USER_MODEL = 'user_mgmt.Users'
AUTH_PERMS_ENABLED =False
AUTH_PERMS = ['']

JWT_VERIFY_EXPIRATION = False
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True, # IAT expiry validation
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_LEEWAY': 0,
    'JWT_ALLOW_REFRESH': False,
    'JWT_EXPIRATION_DELTA': timedelta(seconds=604800),
    'JWT_AUTH_HEADER_PREFIX': 'AUTH',
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(seconds=604800)
}
MAIL_EXPIRATION_TIME = timedelta(seconds=604800)

AES_SECRET_KEY = os.environ.get('AES_SECRET_KEY')

# DjangoSecureApp Configs
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Melbourne'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ENV = os.environ.get('ENV')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

COOKIE_MAX_AGE = 365 * 24 * 60 * 60
COOKIE_KEY = "dpx"
COOKIE_DOMAIN = "dp.exchange"

# Celery Config
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Unit TestCases
TESTING = 'test' in sys.argv
if TESTING:
    TEST_RUNNER = 'test.test_runner.CustomDBTestRunner'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test_dealmax',
            'USER': 'dealmax',
            'PASSWORD': 'dealmax',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

COVERAGE_EXCLUDES_FOLDERS = ['home_loans/migrations/*']

# Encryption Keys
AES_ENC_KEY = os.environ.get('AES_ENC_KEY')

CORS_ORIGIN_ALLOW_ALL = True

DPX_LOGGING_CONFIG = {
    'loggerName': 'dpx_home_loans',
    'loggingConfigPath': BASE_DIR+"/conf/logging.yaml"
}

# Email Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@dealmax.com.au'

APP_DOMAIN = "api.dealmax.com.au"

FACT_FINDER_NOTIFY_DEFAULT_RECIPIENT = ["mark.shwaros@dealmax.com.au"]
