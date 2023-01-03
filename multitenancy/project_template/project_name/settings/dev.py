from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "{{ secret_key }}"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

TENANT_USERS_DOMAIN = "{{domain}}"



DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': '{{database}}',
        'USER': 'postgres',
        'PASSWORD': '{{password}}',
        'HOST': 'localhost',
        'PORT': '{{port}}'
    }
}


try:
    from .local import *
except ImportError:
    pass