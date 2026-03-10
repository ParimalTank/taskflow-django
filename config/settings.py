"""
Django settings for config project.
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Environment Variables ───────────────────────────────────────────
# django-environ reads from .env file and provides typed access
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']


# ─── Installed Apps ──────────────────────────────────────────────────
# Django's INSTALLED_APPS tells Django which apps to include.
# Order matters: Django apps first, then third-party, then your apps.
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',        # Admin panel
    'django.contrib.auth',         # Authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static file serving

    # Third-party apps
    'rest_framework',              # Django REST Framework for APIs

    # Our apps
    'accounts',                    # User auth (register, login, logout)
    'organizations',               # Organizations & memberships
    'boards',                      # Project boards
    'tasks',                       # Tasks within boards
]


# ─── Middleware ──────────────────────────────────────────────────────
# Middleware processes every request/response. Think of it as layers
# that wrap around your views.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'


# ─── Templates ───────────────────────────────────────────────────────
# DIRS tells Django where to look for templates.
# We use a global 'templates/' folder at the project root.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-level templates
        'APP_DIRS': True,                   # Also look in app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ─── Database (Supabase PostgreSQL) ─────────────────────────────────
# Supabase provides a full PostgreSQL database.
# DATABASE_URL format: postgres://USER:PASSWORD@HOST:PORT/DBNAME
# Get this from: Supabase Dashboard > Project Settings > Database
DATABASES = {
    'default': env.db('DATABASE_URL'),
}


# ─── Password Validation ────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── Internationalization ───────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ─── Static Files ───────────────────────────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Project-level static files
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Collected static files for production


# ─── Auth Redirects ─────────────────────────────────────────────────
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/orgs/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# ─── Django REST Framework ──────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# ─── Default Primary Key ────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
