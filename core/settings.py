import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Core Security Configurations
SECRET_KEY = "django-insecure-g8^9(oqos)2*%5_b=p#xc)d*=r6l-luo7wv&-voi9do)2l$(16"
DEBUG = True

# 🌐 FIXED: Wildcard allows your mobile phone and other devices to connect safely over Wi-Fi
# Change this line in settings.py:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']



# Core Application Definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',  # Your application module register
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Unified tracking arrays to catch all template folders securely
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'portal', 'templates'),
            os.path.join(BASE_DIR, 'portal', 'templates', 'portal'),
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Persistence Architecture
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Identity Security Controls
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Regionalization Environment
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# Static Asset Pipelines
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media Upload Channels (For Face ID Biometric Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Identity Routing Controls
LOGIN_URL = 'portal_login'
LOGIN_REDIRECT_URL = 'portal_dashboard'
LOGOUT_REDIRECT_URL = 'portal_login'

# Primary Key Engine Default
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Financial Integration Gateways (Paystack)
PAYSTACK_PUBLIC_KEY = "pk_test_placeholder_your_public_key_string"
PAYSTACK_SECRET_KEY = "sk_test_placeholder_your_secret_key_string"
