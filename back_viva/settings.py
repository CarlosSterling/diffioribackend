"""
Django settings for back_viva project (desarrollo local)
"""

from pathlib import Path
import os
import datetime
import environ

# ────────────────────────────────────────────────────────────
# Rutas y entorno
# ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "change-me"),
    ALLOWED_HOSTS=(str, ""),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
)

# Cargar .env si existe
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env.bool("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,api-diffiori,web-diffiori").split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
# ────────────────────────────────────────────────────────────
# Aplicaciones
# ────────────────────────────────────────────────────────────
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.content.apps.ContentConfig",
    "apps.catalog",
    "apps.clients",
    "apps.blog",
    "apps.core",
    "apps.orders.apps.OrdersConfig",
    "apps.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS
INSTALLED_APPS += ["corsheaders"]

# ────────────────────────────────────────────────────────────
# Middleware y BASICS
# ────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Eliminado: CORS_ALLOW_ALL_ORIGINS = True (Riesgo de seguridad Crítico)
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080"
).split(",")

ROOT_URLCONF = "back_viva.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "back_viva.wsgi.application"

# ─── Custom User Model ───
AUTH_USER_MODEL = "users.User"

# ────────────────────────────────────────────────────────────
# Base de datos
# ────────────────────────────────────────────────────────────
DATABASES = {"default": env.db("DATABASE_URL")}

# ────────────────────────────────────────────────────────────
# Passwords
# ────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ────────────────────────────────────────────────────────────
# Internacionalización
# ────────────────────────────────────────────────────────────
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# ────────────────────────────────────────────────────────────
# Static & Media (desarrollo local)
# ────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ────────────────────────────────────────────────────────────
# Django REST Framework + JWT
# ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=4),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ────────────────────────────────────────────────────────────
# drf-spectacular
# ────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "Diffiori API",
    "DESCRIPTION": "Catálogo de productos, clientes y blog de café especial",
    "VERSION": "0.1.0",
}

# ────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ────────────────────────────────────────────────────────────
# Wompi Payment Gateway
# ────────────────────────────────────────────────────────────
WOMPI_PUBLIC_KEY    = os.environ.get("WOMPI_PUBLIC_KEY", "")
WOMPI_PRIVATE_KEY   = os.environ.get("WOMPI_PRIVATE_KEY", "")
WOMPI_EVENTS_KEY    = os.environ.get("WOMPI_EVENTS_KEY", "")
WOMPI_INTEGRITY_KEY = os.environ.get("WOMPI_INTEGRITY_KEY", "")
WOMPI_BASE_URL      = os.environ.get("WOMPI_BASE_URL", "https://sandbox.wompi.co/v1")
WOMPI_REDIRECT_URL  = os.environ.get("WOMPI_REDIRECT_URL", "http://localhost:3000/checkout/return")

# ────────────────────────────────────────────────────────────
# Jazzmin Admin Theme
# ────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Diffiori Café | Admin",
    "site_header": "Diffiori",
    "site_brand": "Diffiori Café",
    "site_icon": "img/favicon.ico",
    "site_logo": "img/brand-logo.jpg",
    "login_logo": "img/brand-logo.jpg",
    "welcome_sign": "",
    "copyright": "Diffiori Café © 2024",
    "search_model": "catalog.Product",
    "user_avatar": None,

    # Links en la parte superior
    "topmenu_links": [
        {"name": "Inicio",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Sitio", "url": "http://localhost:3000", "new_window": True},
        {"name": "Añadir Producto", "url": "admin:catalog_product_add", "icon": "fas fa-plus"},
        {"name": "Añadir Blog Post", "url": "admin:blog_blogpost_add", "icon": "fas fa-pen"},
        {"model": "auth.User"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["core", "clients"],
    "hide_models": ["core.FAQ", "catalog.ProductVariant"],
    "order_with_respect_to": [
        "content",
        "content.HeroSlide", 
        "content.HomeAbout", 
        "content.HomeFeature", 
        "content.HomeCTA", 
        "catalog", 
        "catalog.Product", 
        "catalog.ProductVariant",
        "catalog.Category", 
        "orders",
        "orders.Order",
        "clients", 
        "blog", 
        "auth"
    ],
    
    # Iconos para las apps y modelos
    "icons": {
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user-cog",
        "auth.Group": "fas fa-users-cog",
        "catalog.Product": "fas fa-mug-hot",
        "catalog.ProductVariant": "fas fa-boxes",
        "catalog.ProductImage": "fas fa-camera-retro",
        "clients.Client": "fas fa-handshake",
        "blog.BlogPost": "fas fa-pen-nib",
        "content.HeroSlide": "fas fa-images",
        "content.HomeAbout": "fas fa-info-circle",
        "content.HomeFeature": "fas fa-certificate",
        "content.HomeCTA": "fas fa-bullhorn",
        "orders.Order": "fas fa-shopping-basket",
        "orders.OrderItem": "fas fa-list-ul",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    "related_modal_active": False,
    "custom_css": "css/admin_diffiori_theme.css",
    "custom_js": "js/admin_custom.js",
    "show_ui_builder": False,
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    
    "side_menu_list": [
        {
            "name": "Tienda",
            "icon": "fas fa-shopping-cart",
            "models": ["catalog.Product", "catalog.Category"]
        },
        {
            "name": "Ventas",
            "icon": "fas fa-money-bill-wave",
            "models": ["orders.Order", "orders.OrderItem"]
        },
        {
            "name": "Contenido",
            "icon": "fas fa-edit",
            "models": ["blog.BlogPost"]
        },
        {
            "name": "Web & Diseño",
            "icon": "fas fa-desktop",
            "models": ["content.HeroSlide", "content.HomeAbout", "content.HomeFeature", "content.HomeCTA"]
        },
        {
            "name": "Seguridad",
            "icon": "fas fa-lock",
            "models": ["auth.User", "auth.Group"]
        },
    ],
    "use_google_fonts": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
