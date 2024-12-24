"""
Django settings for PhotoShopProject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os




BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dl6-j=*q*&d8@&$v$rk@@v)xtwhx+wizy8)b+rcu1f-@@sfe$a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['13.60.235.143', 'localhost', '127.0.0.1','vickyneophotography.com', 'www.vickyneophotography.com']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'UserPage',
    'EmailConfiguration',
    'django_celery_results',
    'django_celery_beat'
]
JAZZMIN_SETTINGS = {
    "site_logo": "logos/logo-footer.jpg",  # Path relative to your static files
    "site_logo_classes": "rounded-circle",  # Optional: additional CSS classes for your logo

    "site_title": "Admin",
    "site_header": "Administration",
    "site_brand": "Vickyneo Photography",
    "welcome_sign": "Welcome! Back Vickyneo",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "custom_css": "css/custom_admin.css",  # Path to the custom CSS file
    "custom_js": "js/custom_admin.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    "brand_logo": "vickytitlelogo.png",  # Path relative to your static files
    "brand_logo_classes": "img-circle",  # Optional: additional CSS classes for your logo
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'EmailConfiguration.middleware.AutoLogoutMiddleware',
    'EmailConfiguration.middleware.TimeZoneMiddleware',
    
]

ROOT_URLCONF = 'PhotoShopProject.urls'

# Template directories
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'website', 'templates'),  # Website app templates
            os.path.join(BASE_DIR, 'UserPage', 'templates'),  # UserPage app templates
        ],
        'APP_DIRS': True,  # Enable searching for templates in app directories
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

WSGI_APPLICATION = 'PhotoShopProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'website', 'static'),  # Website app static files
    os.path.join(BASE_DIR, 'UserPage', 'static'),  # UserPage app static files
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

APPEND_SLASH = False  # Disable appending slashes

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

THUMBNAIL_ALIASES = {
    "": {
        "small": {"size": (150,150)}
  },
}


# Set the session timeout in seconds
SESSION_COOKIE_AGE = 3600  # 1 hour (change as needed)

# Optional: If you want to clear the session on browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# In settings.py
LOGIN_URL = '/Userlogin/'

DATA_UPLOAD_MAX_NUMBER_FILES = 2000  # Increase this value as needed

#celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379'  # Redis as broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TIMEZONE='Asia/Kolkata'

CELERY_RESULT_BACKEND='django-db'


#celery beat
CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 4000  # Adjust this value as needed
