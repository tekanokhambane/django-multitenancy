import hashlib

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.http import urlencode
from django.contrib.auth import get_user_model
from django.db import connection
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
)
from tenant_users.permissions.models import UserTenantPermissions
from tenant_users.tenants.models import ExistsError
from multitenancy.subscriptions.models import Subscription
from multitenancy.apps.models import Tenant

def get_gravatar_url(email, size=50):
    default = "mm"
    size = int(size) * 2  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = getattr(settings, 'MULTITENANCY_GRAVATAR_PROVIDER_URL', '//www.gravatar.com/avatar')

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip('/'),
        hash=hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
        params=urlencode({'s': size, 'd': default})
    )

    return gravatar_url



def create_public_tenant(domain_url, owner_email, password, **owner_extra):
    UserModel = get_user_model()
    TenantModel = get_tenant_model()
    public_schema_name = get_public_schema_name()

    if TenantModel.objects.filter(schema_name=public_schema_name).first():
        raise ExistsError('Public tenant already exists')

    # Create public tenant user. This user doesn't go through object manager
    # create_user function because public tenant does not exist yet
    profile = UserModel.objects.create(
        type="Admin",
        email=owner_email,
        password=make_password(password),
        is_active=True,
        **owner_extra,
    )
    #profile.set_unusable_password()
    profile.save()

    #create a subscription
    subscription = Subscription.objects.create()    

    # Create public tenant
    public_tenant = TenantModel.objects.create(
        schema_name=public_schema_name,
        name='Public Tenant',
        type='public',
        owner=profile,
        subscription=subscription
    )

    

    # Add one or more domains for the tenant
    get_tenant_domain_model().objects.create(
        domain=domain_url,
        tenant=public_tenant,
        is_primary=True,
    )

    # Add system user to public tenant (no permissions)
   # public_tenant.add_user(profile)

    # add user perms
    user_perms = UserTenantPermissions.objects.create(profile_id=profile.pk, is_staff=True, is_superuser=True)