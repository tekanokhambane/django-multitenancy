import hashlib

from django.conf import settings
from django.utils.http import urlencode


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