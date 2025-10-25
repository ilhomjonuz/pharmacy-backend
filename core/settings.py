import os
from pathlib import Path

from corsheaders.defaults import default_headers
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env_path = os.path.join(BASE_DIR, "envs", ".env")
env.read_env(env_path)

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Accept-Language',
    'X-Secret',

]
CORS_ALLOW_CREDENTIALS = True


INSTALLED_APPS = [
    "jazzmin",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "apps.shared.apps.SharedConfig",
    "apps.apteka.apps.AptekaConfig",
    "rest_framework",
    'corsheaders',
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('MYSQL_DATABASE'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': env.str('MYSQL_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TITLE": "Django Rest API",
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "uz-uz"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('uz', _('Uzbek')),
    ('en', _('English')),
    ('ru', _('Russian')),
]

MODEL_TRANSLATION_DEFAULT_LANGUAGE = 'uz'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_UPLOAD_PATH = "uploads/"

STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/bot/media/"
MEDIA_ROOT = BASE_DIR / 'bot' / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 7200,  # Kesh 2 soat davomida saqlanadi, keyin tozalanadi
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "Django Admin",
    "site_header": "Django Admin",
    "site_brand": "Django Admin",
    "site_icon": "/image/logo.png",
    "welcome_sign": "Welcome to Django Admin",
    "topmenu_links": [
        {"name": "Home", "url": "/", "new_window": False},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "auth.Permission": "fas fa-lock",
        "web": "fas fa-globe",
        "web.Home": "fas fa-home",
        "web.About": "fas fa-info-circle",
        "web.SiteUsers": "fas fa-users",
        "SupportBot": "fas fa-robot",
        "SupportBot.BotUsers": "fas fa-robot",
        "SupportBot.TelegramGroupID": "fas fa-users",
        "SupportBot.TelegramChannelID": "fas fa-users",
        "SupportBot.DailyMessages": "fas fa-envelope",
    },
    "copyright": "ShinzoFamily",
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "site_logo_classes": "img-circle",
    "login_logo": "/image/logo.png",
    "custom_css": "/css/jazzmin.css",
    "site_logo": "/image/logo.png",
    "login_logo_dark": "/image/logo.png",
    "show_ui_builder": False,
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}
