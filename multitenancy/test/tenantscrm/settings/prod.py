import os
import environ
import google.auth

from pathlib import Path
from django.utils.translation import gettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import sys
sys.setrecursionlimit(10000)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import environ
import google.auth
 
env = environ.Env()

from google.oauth2 import service_account
import dj_database_url

TENANT_APPS_DIR = os.path.join(PROJECT_DIR, os.pardir)
sys.path.insert(0, TENANT_APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['panel.cloudasync.com']

# Application definition

HAS_MULTI_TYPE_TENANTS = True
MULTI_TYPE_DATABASE_FIELD = 'type'  # or whatever the name you call the database field

TENANT_TYPES = {
    "public": {  # this is the name of the public schema from get_public_schema_name
        "APPS": [
    'django_tenants',
    'rest_framework',

    'django.contrib.staticfiles',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
    'tenant_users.tenants', # defined only in shared apps
    
    #'account',
    # 'guardian',
    'django_countries',
    "phonenumber_field",
   # 'phonenumbers',
    "bootstrap4",
    'formtools',
    'sweetify',
    #'djmoney',
    #'mptt',
    # mandatory
    'django_tenants_portal.cart',
    'django_tenants_portal.teams',
    'django_tenants_portal.customers',
    'django_tenants_portal.users',
    'django_tenants_portal.portal',
   'django_tenants_portal.billing',
   'django_tenants_portal.accounts',
    'services',
    'guardian',
    'groups_manager',
    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.google',

    #helpdesk
    'pinax.teams',
    'pinax.invitations',
    'account',
    'django.contrib.humanize',  # Required for elapsed time formatting
    'markdown_deux',  # Required for Knowledgebase item formatting
    'bootstrap4form', # Required for nicer formatting of forms with the default templates
    'helpdesk',  # This is us!
    
    # Django
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
                  # shared apps here
                  ],
        "URLCONF": "tenantscrm.public_urls", # url for the public type here
    },
    "personal": {
        "APPS": [
            'rest_framework',
            'tenant_users.permissions',

            'website',
            # CodeRed CMS
            'kitsocms',
            'rest_framework',
            'search',
            'wagtailmenus',
            'taggit',
            'colorfield',
            'bootstrap4',
            'wagtailstreamforms',
            

            'storages',

            # allauth
            #'allauth',
            #'allauth.account',
            #'allauth.socialaccount',
            #'allauth.socialaccount.providers.facebook',
            #'allauth.socialaccount.providers.google',

            # Wagtail
            'wagtail.api.v2',
            'wagtail.contrib.forms',
            'wagtail.contrib.redirects',
            'wagtail.embeds',
            'wagtail.sites',
            'wagtail.users',
            'wagtail.snippets',
            'wagtail.documents',
            'wagtail.images',
            'wagtail.search',
            'wagtail.admin',
            'wagtail.core',
            'wagtailcache',
            'wagtail.contrib.settings',
            'wagtail.contrib.modeladmin',
            'wagtailimportexport',
            'wagtail.contrib.table_block',
            'wagtailfontawesome',
            'modelcluster',
            'wagtail_ckeditor',


            # Dango
            'django.contrib.sites',
            'django.contrib.auth',
            'django.contrib.admin',
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

                'website',
                # CodeRed CMS
                'kitsocms',
                'rest_framework',
                'search',
                'wagtailmenus',
                'taggit',
                'colorfield',
                'bootstrap4',
                'wagtailstreamforms',
                #maarifa_store
                'maarifa_store.core',
                'maarifa_store.attribute',
                'maarifa_store.catalog',
                'maarifa_store.checkout',
                'maarifa_store.product',
                'maarifa_store.orders',
                'maarifa_store.shipping',
                'maarifa_store.basket',
                'maarifa_store.configuration',
                'maarifa_store.stats',
                # External apps

            # 'wagtailuiplus',
                #'django_social_share',
                'wagtail_blocks',
                'storages',
                "django_measurement",
                "django_prices",
                "django_prices_openexchangerates",
                "django_prices_vatlayer",
                "django_countries",
                "django_filters",
                "phonenumber_field",
                'wagtailmodelchooser',
                'mjml',
                'birdsong',

                # allauth
               # 'allauth',
               ## 'allauth.account',
               # 'allauth.socialaccount',
               # 'allauth.socialaccount.providers.facebook',
               # 'allauth.socialaccount.providers.google',

                # Wagtail
                'wagtail.api.v2',
                'wagtail.contrib.forms',
                'wagtail.contrib.redirects',
                'wagtail.embeds',
                'wagtail.sites',
                'wagtail.users',
                'wagtail.snippets',
                'wagtail.documents',
                'wagtail.images',
                'wagtail.search',
                'wagtail.admin',
                'wagtail.core',
                'wagtailcache',
                'wagtail.contrib.settings',
                'wagtail.contrib.modeladmin',
                'wagtailimportexport',
                'wagtail.contrib.table_block',
                'wagtailfontawesome',
                'modelcluster',
                'wagtail_ckeditor',


                # Dango
                'django.contrib.sites',
                'django.contrib.auth',
                'django.contrib.admin',
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

                'website',
                # CodeRed CMS
                'kitsocms',
                'rest_framework',
                'search',
                'wagtailmenus',
                'wagtail_marketing',
                'wagtail_marketing.campaign',
                'taggit',
                'colorfield',
                'bootstrap4',
                'wagtailstreamforms',
                #maarifa_store
                'maarifa_store.core',
                'maarifa_store.attribute',
                'maarifa_store.catalog',
                'maarifa_store.checkout',
                'maarifa_store.product',
                'maarifa_store.orders',
                'maarifa_store.shipping',
                'maarifa_store.basket',
                'maarifa_store.configuration',
                'maarifa_store.stats',
                # External apps

                # 'wagtailuiplus',

                #'django_social_share',
                'wagtail_blocks',
                'storages',
                "django_measurement",
                "django_prices",
                "django_prices_openexchangerates",
                "django_prices_vatlayer",
                "django_countries",
                "django_filters",
                "phonenumber_field",
                'wagtailmodelchooser',
                'mjml',
                'birdsong',

                # allauth
               # 'allauth',
               # 'allauth.account',
               # 'allauth.socialaccount',
               # 'allauth.socialaccount.providers.facebook',
               # 'allauth.socialaccount.providers.google',

                # Wagtail
                'wagtail.api.v2',
                'wagtail.contrib.forms',
                'wagtail.contrib.redirects',
                'wagtail.embeds',
                'wagtail.sites',
                'wagtail.users',
                'wagtail.snippets',
                'wagtail.documents',
                'wagtail.images',
                'wagtail.search',
                'wagtail.admin',
                'wagtail.core',
                'wagtailcache',
                'wagtail.contrib.settings',
                'wagtail.contrib.modeladmin',
                'wagtailimportexport',
                'wagtail.contrib.table_block',
                'wagtailfontawesome',
                'modelcluster',
                'wagtail_ckeditor',


                # Dango
                'django.contrib.sites',
                'django.contrib.auth',
                'django.contrib.admin',
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
    'wagtailcache.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #'django_tenants_portal.core.LoginCheckMiddleware.LoginCheckMiddleware',
     # CMS functionality
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    # Fetch from cache. Must be LAST.
    'wagtailcache.cache.FetchFromCacheMiddleware',
]

MIDDLEWARE_CLASSES = [
    "account.middleware.ExpiredPasswordMiddleware",
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",

]

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True


#HELPDESK_VIEW_A_TICKET_PUBLIC = False
#HELPDESK_SUBMIT_A_TICKET_PUBLIC= False

#EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend’"
#EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

EMAIL_HOST = "webmail.bubbledigital.co.za"
EMAIL_PORT = 587
EMAIL_HOST_USER = "noreply@bubbledigital.co.za"
EMAIL_HOST_PASSWORD = "Koketso325"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "No Reply <noreply@bubbledigital.co.za>"




MJML_BACKEND_MODE = 'tcpserver'
MJML_TCPSERVERS = [
    ('127.0.0.1', 28101),  # host and port
]


SITE_ID = 1

LOGIN_URL = "/"
LOGIN_REDIRECT_URL="/"

TENANT_USERS_DOMAIN = "cloudasync.com"

CART_SESSION_ID = 'cart'


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "customers.Client"  # app.Model

TENANT_DOMAIN_MODEL = "customers.Domain"  # app.Model

AUTH_USER_MODEL = 'users.TenantUser'

AUTHENTICATION_BACKENDS = (
    'tenant_users.permissions.backend.UserBackend',
    'guardian.backends.ObjectPermissionBackend',
  #  'allauth.account.auth_backends.AuthenticationBackend',

    # 'django.contrib.auth.backends.ModelBackend',

)
ROOT_URLCONF = 'tenantscrm.public_urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(PROJECT_DIR, 'templates')],
        #'APP_DIRS': False,
        'OPTIONS': {
            "loaders": [
                "django_tenants.template.loaders.filesystem.Loader",  # Must be first
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "account.context_processors.account",
                'wagtailmenus.context_processors.wagtailmenus',
                'maarifa_store.configuration.context_processors.currency'
              
            ],
            
        },
    },
]


MULTITENANT_TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, 'tenants/%s/templates')
]


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

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

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

#MEDIA_URL= '/media/'

STATIC_ROOT=os.path.join(PROJECT_DIR,"static")

STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",  # Must be first
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
#GS_PROJECT_ID = 'ancient-lattice-288821'
#S_MEDIA_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME", None)
GS_BUCKET_NAME = env("GS_BUCKET_NAME", None)
STATIC_URL = 'https://storage.googleapis.com/{}/'.format(
    GS_BUCKET_NAME)
#MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(
#    GS_MEDIA_BUCKET_NAME)
GS_DEFAULT_ACL = 'publicRead'
GS_FILE_OVERWRITE = False
#GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#    GOOGLE_APPLICATION_CREDENTIALS
# )

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True  


# or this way

#STATICFILES_FINDERS.insert(0, "django_tenants.staticfiles.finders.TenantFileSystemFinder")

MULTITENANT_STATICFILES_DIRS = [
    os.path.join( PROJECT_DIR, "tenants/%s/static" ),
]

#STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"

MULTITENANT_RELATIVE_STATIC_ROOT = ""  # (default: create sub-directory for each tenant)

MULTITENANT_RELATIVE_MEDIA_ROOT = ""

#STATICFILES_DIRS = [
#    BASE_DIR ="static",
#]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wagtail
WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ('streamforms/form_block.html', 'Default Form Template'),  # default
    ('streamforms/form_block_inline.html', 'Inline Form Template'),
)

PRODUCT_VARIANT_MODEL = 'catalog.ProductVariant'

MJML_BACKEND_MODE = 'tcpserver'
MJML_TCPSERVERS = [
    ('127.0.0.1', 28101),  # host and port
]

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail_ckeditor.widgets.CKEditor'
    }
}

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_FRAME_DENY = True

WAGTAIL_CKEDITOR_USE_MATH = True

WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
WAGTAIL_PASSWORD_RESET_ENABLED = False
WAGTAIL_SITE_NAME = "Maarifa cms"

WAGTAIL_USER_EDIT_FORM = 'maarifa_store.core.forms.TenantUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'maarifa_store.core.forms.TenantUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = []
PRODUCT_VARIANT_MODEL = 'catalog.ProductVariant'
DEFAULT_MAX_DIGITS = 12

# Bootstrap

BOOTSTRAP4 = {
    # set to blank since coderedcms already loads jquery and bootstrap
    'jquery_url': '',
    'base_url': '',
    # remove green highlight on inputs
    'success_css_class': ''
}


# Tags
#SESSION_COOKIE_DOMAIN = '.localhost'
TAGGIT_CASE_INSENSITIVE = True
BASE_URL = 'https://panel.cloudasync.com'
PAYFAST_URL_BASE = 'https://panel.cloudasync.com'
PAYFAST_TEST_MODE = True
PAYFAST_MERCHANT_ID = env('PAYFAST_MERCHANT_ID')
PAYFAST_MERCHANT_KEY = env('PAYFAST_MERCHANT_KEY')
HELPDESK_PUBLIC_TICKET_DUE_DATE = False
HELPDESK_VIEW_A_TICKET_PUBLIC = True