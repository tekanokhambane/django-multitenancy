# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from multitenancy.helpdesk.models import Queue
from multitenancy.helpdesk.tests.helpers import get_user


class TestSavingSharedQuery(TestCase):
    def setUp(self):
        q = Queue(title='Q1', slug='q1')
        q.save()
        self.q = q

    def test_cansavequery(self):
        """Can a query be saved"""
        url = reverse('multitenancy.helpdesk:savequery')
        self.client.login(username=get_user(is_staff=True).get_username(),
                          password='password')
        response = self.client.post(
            url,
            data={
                'title': 'ticket on my queue',
                'queue': self.q,
                'shared': 'on',
                'query_encoded':
                    'KGRwMApWZmlsdGVyaW5nCnAxCihkcDIKVnN0YXR1c19faW4KcDMKKG'
                    'xwNApJMQphSTIKYUkzCmFzc1Zzb3J0aW5nCnA1ClZjcmVhdGVkCnA2CnMu'
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('tickets/?saved_query=1' in response.url)
