import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import sys
sys.setrecursionlimit(10000)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



import environ
 
env = environ.Env()
TENANT_APPS_DIR = os.path.join(PROJECT_DIR, os.pardir)
sys.path.insert(0, TENANT_APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

HAS_MULTI_TYPE_TENANTS = True
MULTI_TYPE_DATABASE_FIELD = 'type'  # or whatever the name you call the database field

TENANT_TYPES = {
    "public": {  # this is the name of the public schema from get_public_schema_name
        "APPS": [
            # mandatory
            'django_tenants',
            'tenant_users.permissions', # Defined in both shared apps and tenant apps
            'tenant_users.tenants.apps.TenantsConfig', # defined only in shared apps
            
            # multitenancy
            'multitenancy.users',
            'multitenancy.core',
            'multitenancy.subscriptions.apps.SubscriptionsConfig',
            'multitenancy.apps',
            'multitenancy.admin',
            'multitenancy.group.apps.GroupConfig',
            'multitenancy.profiles',
            'multitenancy.settings',

            # 3rd party apps
            'rest_framework',
            'reversion',
            'django_countries',
            'django_crontab',
            "phonenumber_field",
            'easy_thumbnails',
            
            'django_redis',
            'django_select2',
            "bootstrap4",
            'formtools',
            'sweetify',
            'widget_tweaks',
            'django_extensions',
            'guardian',
            'groups_manager',
            'account',
            'pinax.teams',
            'pinax.invitations',
            'django.contrib.humanize',  # Required for elapsed time formatting
            'markdown_deux',  # Required for Knowledgebase item formatting
            'bootstrap4form', # Required for nicer formatting of forms with the default templates
            'helpdesk',
            # Django
            'django.contrib.sites',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.sitemaps',
            'django.contrib.auth',
            'django.contrib.staticfiles',
            'django.contrib.contenttypes',
                  # shared apps here
                  ],
        "URLCONF": "tenantscrm.public_urls", # url for the public type here
    },
    "personal": {
        "APPS": [
            'tenant_users.permissions',

            'rest_framework',

            'storages',
            # Dango
            'django.contrib.sites',
            'django.contrib.auth',
            'django.contrib.messages',
            'django.contrib.sitemaps',
            'django.contrib.staticfiles',
            'django.contrib.contenttypes',
                 # type1 apps here
                 ],
        "URLCONF": "tenantscrm.urls",
    },
    "premium": {
        "APPS": [
                'rest_framework',
                'tenant_users.permissions',


                

                # Dango
                'django.contrib.sites',
                'django.contrib.auth',
                'django.contrib.messages',
                'django.contrib.sitemaps',
                'django.contrib.staticfiles',
                'django.contrib.contenttypes',
                 # type1 apps here
                 ],
        "URLCONF": "tenantscrm.urls_premium",
    },
    "business": {
        "APPS": [
                'rest_framework',
                'tenant_users.permissions',




                # Dango
                'django.contrib.sites',
                'django.contrib.auth',
                'django.contrib.messages',
                'django.contrib.sitemaps',
                'django.contrib.staticfiles',
                'django.contrib.contenttypes',
                 # type1 apps here
                 ],
        "URLCONF": "tenantscrm.urls_business",
    }
}


INSTALLED_APPS = []
for schema in TENANT_TYPES:
    INSTALLED_APPS += [app for app in TENANT_TYPES[schema]["APPS"] if app not in INSTALLED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "multitenancy.settings.middleware.TeamMiddleware",

]

MIDDLEWARE_CLASSES = [
#    "account.middleware.ExpiredPasswordMiddleware",
    "account.middleware.ExpiredPasswordMiddleware",
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",

]

ACCOUNT_EMAIL_UNIQUE = False
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False


LOGIN_URL = "accounts_login"
LOGIN_REDIRECT_URL="accounts_login"
ACCOUNT_LOGOUT_REDIRECT_URL = "accounts_login"



DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "apps.Tenant"  # app.Model

TENANT_DOMAIN_MODEL = "apps.Domain"  # app.Model

AUTH_USER_MODEL = 'users.TenantUser'

AUTHENTICATION_BACKENDS = (
    'tenant_users.permissions.backend.UserBackend',
    'account.auth_backends.EmailAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',

)
ROOT_URLCONF = 'tenantscrm.urls'
#PUBLIC_SCHEMA_URLCONF = 'tenantscrm.public_urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "account.context_processors.account",
            ],
            
        },
    },
]


GROUPS_MANAGER = {
    'AUTH_MODELS_SYNC': True,
}

ACCOUNT_LOGIN_REDIRECT_URL = 'account_login'

ACCOUNT_EMAIL_REQUIRED=True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 
TENANT_LIMIT_SET_CALLS = True

ACCOUNT_AUTHENTICATION_METHOD = "email"

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', _('English'))
]

WSGI_APPLICATION = 'tenantscrm.wsgi.application'

GROUPS_MANAGER = {
'AUTH_MODELS_SYNC': True,
}

CACHES = {
    # … default cache config and others
    "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                }
            },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"
SELECT2_JS = "plugins/select2/js/select2.min.js"
SELECT2_CSS = "plugins/select2/css/select2.min.css"
SELECT2_I18N_PATH = "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/i18n"
# Database
 # https://docs.djangoproject.com/en/3.2/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT=os.path.join(PROJECT_DIR,'media/')



MEDIA_URL= '/media/'

STATIC_URL="/static/"
STATIC_ROOT=os.path.join(PROJECT_DIR,"static")

STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",  # Must be first
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


MULTITENANT_STATICFILES_DIRS = [
    os.path.join( PROJECT_DIR, "tenants/%s/static" ),
]

STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"

MULTITENANT_RELATIVE_STATIC_ROOT = ""  # (default: create sub-directory for each tenant)

MULTITENANT_RELATIVE_MEDIA_ROOT = ""


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



TAGGIT_CASE_INSENSITIVE = True
HELPDESK_PUBLIC_TICKET_DUE_DATE = False
HELPDESK_VIEW_A_TICKET_PUBLIC = True

TENANT_DISPLAY_NAME = "Service"
TENANT_DISPLAY_NAME_PLURAL = "Services"

# possible options: 'sweetalert', 'sweetalert2' - default is 'sweetalert2'
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'