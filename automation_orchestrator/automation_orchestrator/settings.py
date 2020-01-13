"""
Django settings for automation_orchestrator project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket


# Retrieve the secret key for the server.
def get_secret_key():
    env_var_name = "BASICO_AUTOMATIONORCHESTRATOR_SECRET_KEY"

    if not env_var_name in os.environ:
        secret_key = generate_secret_key(env_var_name)

    else:
        try:
            secret_key = os.environ[env_var_name]
        except:
            secret_key = generate_secret_key(env_var_name)

    return secret_key


# Generate secret key for the server.
def generate_secret_key(env_var_name):
    import subprocess
    from django.core.management.utils import get_random_secret_key

    secret_key = get_random_secret_key()

    subprocess.run(['setx', env_var_name, secret_key], stdout=subprocess.PIPE)

    print(f"""
***

A secret key for encrypting data in the database has been generated.
This key is securily stored as an environment variable with the name: {env_var_name}

***
""")

    return secret_key


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
                 'localhost',
                 socket.gethostbyname_ex(socket.gethostname())[-1][-1]]

# Application definition

INSTALLED_APPS = [
    'orchestrator.apps.OrchestratorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'admin_reorder',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'automation_orchestrator.urls'

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

WSGI_APPLICATION = 'automation_orchestrator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

def generate_database_folder_structure(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

    if not os.path.exists(os.path.join(folder, 'backup')):
        os.mkdir(os.path.join(folder, 'backup'))

    return os.path.join(folder, DATABASE_NAME)

DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'AutomationOrchestratorDatabase')
DATABASE_NAME = 'db.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': generate_database_folder_structure(DATABASE_DIR),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
                  'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.BasicAuthentication', ),
                  'DEFAULT_THROTTLE_CLASSES': [
                      'rest_framework.throttling.ScopedRateThrottle',
                      ],
                  'DEFAULT_THROTTLE_RATES': {
                      'apitrigger': '1/second',
                      'botflowexecution': '1/second',
                      'pythonfunction': '1/second',
                      'pythonfunctionexecution': '1/second'
                      },
                  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
                  }

ADMIN_REORDER = (
    'auth',

    {'app': 'orchestrator',
     'label': 'Setup',
     'models': ('orchestrator.Bot', 'orchestrator.App', 'orchestrator.Botflow',)},

    {'app': 'orchestrator',
     'label': 'Notifications',
     'models': ('orchestrator.SmtpAccount',)},

    {'app': 'orchestrator',
     'label': 'Triggers',
     'models': ('orchestrator.EmailImapTrigger', 'orchestrator.EmailOutlookTrigger', 'orchestrator.FileTrigger', 'orchestrator.ScheduleTrigger', 'orchestrator.ApiTrigger',)},

    {'app': 'orchestrator',
     'label': 'Botflow Execution Log',
     'models': ('orchestrator.BotflowExecution',)},

    {'app': 'orchestrator',
     'label': 'Python',
     'models': ('orchestrator.PythonFunction', 'orchestrator.PythonFunctionExecution',)}
)
