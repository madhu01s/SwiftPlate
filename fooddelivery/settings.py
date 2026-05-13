"""
Django settings for fooddelivery project.
"""

from pathlib import Path
import os



# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent



# =========================
# TEMPLATE / STATIC / MEDIA
# =========================

TEMPLATES_DIR = os.path.join(
    BASE_DIR,
    'templates'
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    'static'
)

MEDIA_ROOT = os.path.join(
    BASE_DIR,
    'media'
)



# =========================
# SECURITY
# =========================

SECRET_KEY = 'django-insecure-9pb#^b0lv#x6(-os5_a93=y3jnq8^5egc8354fw(j4u9h$iv_k'

DEBUG = True

ALLOWED_HOSTS = []



# =========================
# INSTALLED APPS
# =========================

INSTALLED_APPS = [

    # JAZZMIN
    'jazzmin',

    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CUSTOM APPS
    'orders',

]



# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]



# =========================
# ROOT URL CONFIG
# =========================

ROOT_URLCONF = 'fooddelivery.urls'



# =========================
# TEMPLATES
# =========================

TEMPLATES = [

    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS':
            [TEMPLATES_DIR],

        'APP_DIRS':
            True,

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



# =========================
# WSGI APPLICATION
# =========================

WSGI_APPLICATION = 'fooddelivery.wsgi.application'



# =========================
# DATABASE
# =========================

DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.sqlite3',

        'NAME':
            BASE_DIR / 'db.sqlite3',

    }

}



# =========================
# MYSQL CONFIG (OPTIONAL)
# =========================

"""
DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.mysql',

        'NAME':
            'fooddelivery_db',

        'USER':
            'root',

        'PASSWORD':
            'your_password',

        'HOST':
            'localhost',

        'PORT':
            '3306',

    }

}
"""



# =========================
# PASSWORD VALIDATORS
# =========================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]



# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



# =========================
# STATIC FILES
# =========================

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    STATIC_DIR
]



# =========================
# MEDIA FILES
# =========================

MEDIA_URL = '/media/'

MEDIA_ROOT = MEDIA_ROOT



# =========================
# DEFAULT AUTO FIELD
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# =========================
# LOGIN / LOGOUT REDIRECTS
# =========================

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'



# =========================
# STRIPE KEYS
# =========================

STRIPE_PUBLISHABLE_KEY = (
    'your_publishable_key'
)

STRIPE_SECRET_KEY = (
    'your_secret_key'
)



# =========================
# JAZZMIN SETTINGS
# =========================

JAZZMIN_SETTINGS = {

    "site_title":
        "SwiftPlate Admin",

    "site_header":
        "SwiftPlate",

    "site_brand":
        "Food Delivery",

    "welcome_sign":
        "Welcome to SwiftPlate Admin",

    "copyright":
        "SwiftPlate",

    "search_model":
        ["auth.User", "orders.FoodItem"],

    "topmenu_links": [

        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"]
        },

        {
            "model": "auth.User"
        },

        {
            "app": "orders"
        },

    ],

    "show_sidebar":
        True,

    "navigation_expanded":
        True,

    "hide_apps":
        [],

    "hide_models":
        [],

    "order_with_respect_to": [
        "orders",
        "orders.fooditem",
        "orders.order",
        "orders.cart",
    ],

    "icons": {

        "auth":
            "fas fa-users-cog",

        "auth.user":
            "fas fa-user",

        "orders.fooditem":
            "fas fa-hamburger",

        "orders.order":
            "fas fa-shopping-cart",

        "orders.cart":
            "fas fa-cart-plus",

        "orders.useraddress":
            "fas fa-map-marker-alt",

    },

}
# =========================
# STRIPE CONFIG
# =========================

STRIPE_PUBLIC_KEY = ""

STRIPE_SECRET_KEY = ""