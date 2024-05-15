import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "INSECURE")
DEBUG = True if os.environ.get("DEBUG") == '1' else False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    # "daphne", # django-channels
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Personal Apps
    # 'apps.chat.apps.ChatConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.business.apps.BusinessConfig',
    'apps.personal.apps.PersonalConfig',
    # 'apps.users.apps.UsersConfig',
    'apps.general.apps.GeneralConfig',

    #Django allauth apps
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
]


# ASGI_APPLICATION = "setup.asgi.application"

# CHANNEL_LAYERS={
#     'default':{
#         'BACKEND': 'channels.layers.InMemoryChannelLayer'
#     }
#     # 'default':{
#     #     'BACKEND': 'channels_redis.core.RedisChannelLayer',
#     #     'CONFIG':{
#     #         'hosts':[('127.0.0.1', 6379)],
#     #     }
#     # }
# }

# SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Add the account middleware:
    # "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'setup.urls'

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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT':os.environ.get('DATABASE_PORT'),
        # 'OPTIONS': {
        #     'charset': os.environ.get('DATABASE_CHARSET'),
        #     'init_command': os.environ.get('DATABASE_INIT_COMMAND'),
        # }
    }
}

# Used by django-allauth
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]


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


LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Africa/Luanda'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


############################################### Extra Config ##############################################################
# Customized User model
AUTH_USER_MODEL = 'accounts.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'local_static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Ficheiros acima de 2MB vão p/ a o TemporaryMemory, baixo p/ o InMemory
FILE_UPLOAD_MAX_MEMORY_SIZE=2000000

# configuração das mensages de alertas passados nos views
MESSAGE_TAGS ={
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
}

EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS'))
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))

JAZZMIN_SETTINGS = {
    "site_title": "HeadHunter",
    "site_header": "HeadHunter",
    "site_brand": "HeadHunter",
    "site_logo": "assets/images/logo/logo.png",
    "login_logo": "assets/images/logo/logo-horizontal.png",
    "site_icon": "assets/images/logo/logo.png",
    "welcome_sign": "Bem Vindo a Administração do HeadHunter",
    "copyright": "HeadHunter",
}


# CKEDITOR_UPLOAD_PATH = 'media-contents/'
# CKEDITOR_CONFIGS = {
#     'default':{
#         'skin': 'moono',
#         'codeSnippet_theme':'monokai',
#         'toolbar': 'all',
#         'extraPlugins' : ','.join(
#             [
#                 'codesnippet',
#                 'widget',
#                 'dialog'
#             ]
#         ),
#     }
# }

