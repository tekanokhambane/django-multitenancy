# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from helpdesk.models import Queue, Ticket, UserSettings
import sys


User = get_user_model()


def get_user(username='helpdesk.staff',
             password='password',
             is_staff=False,
             is_superuser=False):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email='%s@example.com' % username)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
    else:
        user.set_password(password)
        user.save()
    return user


def get_staff_user():
    return get_user(is_staff=True)


def reload_urlconf(urlconf=None):

    from importlib import reload

    if urlconf is None:
        from django.conf import settings

        urlconf = settings.ROOT_URLCONF

    if HELPDESK_URLCONF in sys.modules:
        reload(sys.modules[HELPDESK_URLCONF])

    if urlconf in sys.modules:
        reload(sys.modules[urlconf])

    from django.urls import clear_url_caches
    clear_url_caches()


def create_ticket(**kwargs):
    q = kwargs.get('queue', None)
    if q is None:
        try:
            q = Queue.objects.all()[0]
        except IndexError:
            q = Queue.objects.create(title='Test Q', slug='test', )
    data = {
        'title': "I wish to register a complaint",
        'queue': q,
    }
    data.update(kwargs)
    return Ticket.objects.create(**data)


HELPDESK_URLCONF = 'helpdesk.urls'


def print_response(response, stdout=False):
    content = response.content.decode()
    if stdout:
        print(content)
    else:
        with open("response.html", "w") as f:  # pragma: no cover
            f.write(content)  # pragma: no cover
