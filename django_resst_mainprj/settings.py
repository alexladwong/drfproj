"""
Django settings for django_resst_mainprj project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gabf_m6@_9k^i)0mh*kbl(zwjnh^y@_w1b^k(ap@6#(0snshfs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # OTP support
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',
    # ''django.contrib.sessions',
    
    # Django Frameworks
     'rest_framework',
     
     # My application
     'studentsapps',
     'api',
]

# INSTALLED_APPS += ['django.contrib.sessions']
# MIDDLEWARE += ['django.contrib.sessions.middleware.SessionMiddleware']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_otp.middleware.OTPMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'django_resst_mainprj.urls'

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

AUTH_USER_MODEL = 'studentsapps.CustomUser'

WSGI_APPLICATION = 'django_resst_mainprj.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIR = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add to urlpatterns
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kintuale@gmail.com'
EMAIL_HOST_PASSWORD = 'ufwnvbxgzmynbjpi'
DEFAULT_FROM_EMAIL = 'Students Systems <kintuale@gmail.com>'
SITE_URL = 'http://127.0.0.1:8000'  # Change in production
SUPPORT_EMAIL = 'umd.developers@gmail.com'

# IP Geolocation settings
IPAPI_TIMEOUT = 5  # seconds

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-location',
    }
}
NOMINATIM_USER_AGENT = "studentsapps" 






# Custom Admin Settings
JAZZMIN_SETTINGS = {
    'site_header': "DRF API's",
    'site_brand': "",
    'site_logo': "/assets/images/logo.png",
    'copyright':  "All Right Reserved 2025",
    "welcome_sign": "Welcome to DRF API's, Login Now.",
    "topmenu_links": [

        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        # {"name": "Company", "url": "/admin/addons/company/"},
        # {"name": "Users", "url": "/admin/userauths/user/"},

        {"model": "AUTH_USER_MODEL.User"},
    ],

    # "order_with_respect_to": [
    #     "hotel",
    #     "hotel.Hotel",
    #     "hotel.Room",
    #     "hotel.Booking",
    #     "hotel.BookingDetail",
    #     "hotel.Guest",
    #     "hotel.RoomServices",
    #     "userauths"
    #     "addons",
    # ],
    "icons": {
        "admin.LogEntry": "fas fa-admin",
        
        "auth.user.Dashboard": "fas fa-file",

        "auth.Group": "fas fa-users-cog",
        "auth.user": "fas fa-user",

        "userauths.User": "fas fa-user",
        "userauths.Profile":"fas fa-address-card",

        "donations.Donation": "fas fa-hand-holding-usd",
        "donations.Payment": "fas fa-credit-card",

        "newsfeed.Newsletter": "fas fa-envelope",
        "newsfeed.SubscribedUser": "fas fa-at",

        "newsfeed.SubscribedUser": "fas fa-at",

        "contacts.Inquiry": "fas fa-phone",
        "addon.BasicAddon": "fas fa-cog",

        "store.Products": "fas fa-product-hunt",
        "store.Order":"fas fa-first-order-alt",
        "store.OrderItem":"fas fa-cart-plus",
        "store.Cart":"fas fa-cart-plus",
        "store.CartOrderItem":"fas fa-shopping-basket",
        "store.Variation":"fas fa-pencil",
        "store.products":"fas fa-cart",
        "store.Review":"fas fa-star fa-beat",
        "store.Category":"fas fa-tag",
        "store.Tag":"fas fa-tag",
        "store.Coupon":"fas fa-gift",
        "store.Gallery":"fas fa-image",
        
        
        "blog.Blog":"fas fa-blog",
        "blog.Comment":"fas fa-comment",
        "blog.Category":"fas fa-cat",
        
        "customer.Address":"fas fa-location",
        "customer.Notification":"fas fa-bell",
        "customer.Wishlist":"fas fa-heart",
        "customer.Notifications":"fas fa-bell",
        

        "vendor.BankAccount":"fas fa-bank",
        "vendor.Notifications":"fas fa-bell",
        "vendor.Payouts":"fa fa-credit-card",
        "vendor.Vendors":"fa fa-industry",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    "related_modal_active": False,
    
    "custom_js": None,
    "show_ui_builder": False,
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}


customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload"
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "underline",
            "|",
            "link",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
    },
}
