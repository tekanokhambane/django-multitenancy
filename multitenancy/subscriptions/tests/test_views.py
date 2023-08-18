from multitenancy.subscriptions.models import Plan
from multitenancy.subscriptions.views import (
    CreatePlanView, 
    PlanDetailView,
    PlanListView,
)
import unittest
from django.test import RequestFactory, TestCase, Client

from multitenancy.users.models import TenantUser

class PlanViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
    def test_get_create_plan_view(self):
        self.user = TenantUser.objects.create_superuser(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='testaadminabc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/billing/plans/create/')
        request.user = self.user
        response = CreatePlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
                                              
    def test_post_create_plan_view(self):
        self.user = TenantUser.objects.create_superuser(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='testadminabc123@email.com', 
            type='Admin',
            is_active=True
            )
        self.client.force_login(user=self.user)
        self.data= {
            "name":"basic",
            "description":"basic plan",
            "price":78,
        }
        request = self.factory.post('/admin/plans/create/', data=self.data)
        request.user = self.user
        response = CreatePlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    
    def test_plan_detail_view(self):
        self.admin = TenantUser.objects.create_superuser(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='test2adminabc123@email.com', 
            type='Admin',
            is_active=True
            )
        self.client.force_login(user=self.admin)
        self.plan = Plan.objects.create(
            name='enterprise',
        )
        self.request = self.factory.get(f'/billing/plans/{self.plan}/')
        self.request.user = self.admin
        view = PlanDetailView.as_view()
        response = view(self.request, pk=self.plan.pk)
        self.assertEqual(response.status_code, 200)
        
