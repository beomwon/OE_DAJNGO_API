from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured
from corsheaders.defaults import default_headers

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
        
ALLOWED_HOSTS = [get_secret("HOST_NAME")]
# ALLOWED_HOSTS = []

SECRET_KEY = get_secret("DJANGO_SECERT_KEY")
ALIGO_APIKEY = get_secret("ALIGO_APIKEY") 
ALIGO_USERID = get_secret("ALIGO_USERID")
ALIGO_SENDERKEY = get_secret("ALIGO_SENDERKEY")
ALIGO_TOKEN = get_secret("ALIGO_TOKEN")
ALIGO_SENDER = get_secret("ALIGO_SENDER")
LOGIN_API_ADDRESS = get_secret("LOGIN_API_ADDRESS")
OE_WORKERS_API_ADDRESS = get_secret("OE_WORKERS_API_ADDRESS")
OE_WORKERS_API_KEY = get_secret("OE_WORKERS_API_KEY")
DATABASES_HOST = get_secret("DATABASES_HOST")
DATABASES_PASSWORD = get_secret("DATABASES_PASSWORD")
DATABASES_PORT = get_secret("DATABASES_PORT") 
JWT_KEY = get_secret("JWT_KEY")
HOLIDAY_URL = get_secret("HOLIDAY_URL")
HOLIDAY_KEY = get_secret("HOLIDAY_KEY")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders', # jwt 토큰으로 로그인 유지
    'user',
    'recommend',
    'store',
    'django_apscheduler'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # jwt 토큰으로 로그인 유지 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'osyulraeng.urls'

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

WSGI_APPLICATION = 'osyulraeng.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'osyulraeng',
        'USER': 'root',
        'HOST': DATABASES_HOST,
        'PASSWORD': DATABASES_PASSWORD,
        'PORT': DATABASES_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [ "GET", "POST", "DELETE", "PATCH", "PUT", "UPDATE", "OPTIONS"]
CORS_ALLOW_HEADERS = list(default_headers) + [
    "token",
]
# 스케줄러
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default
SCHEDULER_DEFAULT = True
