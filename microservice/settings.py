from pathlib import Path
import os
import dj_database_url


# Setup paths
## Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Load settings
if os.path.exists('local_env.py'):
    import local_env
    DEBUG = local_env.DEBUG
    SECRET_KEY = local_env.SECRET_KEY
    DATABASE_URL = local_env.DATABASE_URL
    ALLOWED_HOSTS = local_env.ALLOWED_HOSTS
else:
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
        
if not SECRET_KEY:
    SECRET_KEY = 'django-insecure-%q3&3#hDg7o*=fmj1mDFjdkf8#$%kCvm(_5a9c2)u51gmre((1%w+3nqh!-'
if not DATABASE_URL:
    DATABASE_URL = 'postgres://USER:PASS@microservice-db-srv:9021/microservice'
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')


# Base django settings
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dj_cqrs',
    'backend'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'microservice.urls'
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
WSGI_APPLICATION = 'microservice.wsgi.application'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {}
}
DATABASES['default'].update(dj_database_url.config(default=DATABASE_URL))


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Rest Framework setup
# https://www.django-rest-framework.org/#installation
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


# Django CQRS setup
CQRS = {
    'transport': 'dj_cqrs.transport.RabbitMQTransport',
    'url': 'amqp://guest:guest@message-bus-srv:5672/'
}

