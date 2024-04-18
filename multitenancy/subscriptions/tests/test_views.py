import datetime
import json
import unittest
from unittest.mock import MagicMock, Mock, patch
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import render
import sweetify
from rest_framework.test import force_authenticate
from django.http import HttpRequest, HttpResponseRedirect
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse, reverse_lazy
from multitenancy.users.models import Admin
from multitenancy.subscriptions.filters import PlanFilter
from multitenancy.subscriptions.forms import PlanForm, ProductFeatureForm
from django.contrib.auth.models import AnonymousUser
from multitenancy.subscriptions.models import (
    Plan,
    ProductFeature,
    ProductType,
    Subscription,
)
from multitenancy.subscriptions.serializers import (
    PlanSerialiser,
    ProductTypeSerializer,
    SubscriptionSerializer,
)
from multitenancy.subscriptions.views import (
    DeletePlanView,
    FeatureCreateView,
    PlanDetailView,
    PlanListView,
    PlanView,
    PlanViewSet,
    ProductTypeViewSet,
    SubscriptionsListView,
    UpdatePlanView,
)

User = get_user_model()
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
        self.user = Admin.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="khamban",
            email="testaadminabc123@email.com",
            is_active=True,
        )

        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/billing/plans/create/")
        request.user = self.user
        response = CreatePlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)


#     def test_post_create_plan_view(self):
#         self.user = TenantUser.objects.create_superuser(
#             username="admin",
#             password="password",
#             first_name="abc123",
#             last_name="khamban",
#             email="testadminabc123@email.com",
#             type="Admin",
#             is_active=True,
#         )
#         self.client.force_login(user=self.user)
#         self.data = {
#             "name": "basic",
#             "description": "basic plan",
#             "price": 78,
#         }
#         request = self.factory.post("/admin/plans/create/", data=self.data)
#         request.user = self.user
#         response = CreatePlanView.as_view()(request)
#         self.assertEqual(response.status_code, 200)

#     def test_plan_detail_view(self):
#         self.admin = TenantUser.objects.create_superuser(
#             username="admin",
#             password="password",
#             first_name="abc123",
#             last_name="khamban",
#             email="test2adminabc123@email.com",
#             type="Admin",
#             is_active=True,
#         )
#         self.client.force_login(user=self.admin)
#         self.plan = Plan.objects.create(
#             name="enterprise",
#         )
#         self.request = self.factory.get(f"/billing/plans/{self.plan}/")
#         self.request.user = self.admin
#         view = PlanDetailView.as_view()
#         response = view(self.request, pk=self.plan.pk)
#         self.assertEqual(response.status_code, 200)


# class TestPlanListView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the PlanListView class returns a list of plans when the user is authenticated as an admin.
#     def test_plan_list_view_returns_plans_for_authenticated_admin(self):
#         # Create a mock user with admin privileges
#         user = User.objects.create(username="admin", type="Admin")
#         self.client.force_login(user)

#         # Make a GET request to the PlanListView
#         response = self.client.get(reverse("plan-list"))

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Assert that the response contains the plans
#         self.assertContains(response, "Plan 1")
#         self.assertContains(response, "Plan 2")
#         self.assertContains(response, "Plan 3")

#     # Test that the PlanFilter filters plans by id correctly
#     def test_filter_plans_by_id(self):
#         # Create some plans with different ids
#         plan1 = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Plan 1 description", price=100
#         )
#         plan2 = Plan.objects.create(
#             name="Plan 2", slug="plan-2", description="Plan 2 description", price=200
#         )
#         plan3 = Plan.objects.create(
#             name="Plan 3", slug="plan-3", description="Plan 3 description", price=300
#         )

#         # Create a request with a filter for plan2's id
#         request = self.client.get("/plans/", {"id": plan2.id})

#         # Instantiate the PlanListView and get the context data
#         view = PlanListView()
#         view.request = request
#         context = view.get_context_data()

#         # Get the filtered queryset from the context
#         filtered_queryset = context["filter"].qs

#         # Assert that only plan2 is in the filtered queryset
#         self.assertEqual(len(filtered_queryset), 1)
#         self.assertEqual(filtered_queryset[0], plan2)

#     # Test that PlanListView returns an empty list when no plans exist
#     def test_empty_plan_list(self):
#         # Create an instance of PlanListView
#         view = PlanListView()

#         # Mock the request object
#         request = MagicMock()
#         view.request = request

#         # Mock the GET attribute of the request object
#         request.GET = {}

#         # Mock the PlanFilter object
#         filter = MagicMock()
#         filter.qs = []
#         PlanFilter.return_value = filter

#         # Call the get_context_data method of PlanListView
#         context = view.get_context_data()

#         # Assert that the 'filter' key in the context dictionary is an empty list
#         self.assertEqual(context["filter"], [])

#         # Assert that the queryset attribute of the PlanFilter object was called with the correct arguments
#         filter.qs.assert_called_once_with(Plan.objects.all())

#     # Test that the PlanListView class returns a list of plans when the user is authenticated and is an admin.
#     def test_plan_list_view_returns_plans(self):
#         # Create a user with admin privileges
#         admin_user = User.objects.create(username="admin", type="Admin")
#         admin_user.set_password("admin123")
#         admin_user.save()

#         # Log in the admin user
#         self.client.login(username="admin", password="admin123")

#         # Make a GET request to the PlanListView
#         response = self.client.get("/plans/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the response contains the plans
#         self.assertContains(response, "Plan 1")
#         self.assertContains(response, "Plan 2")
#         self.assertContains(response, "Plan 3")

#     # Test that the PlanListView redirects to the login page when the user is not authenticated
#     def test_redirect_to_login_page_when_user_not_authenticated(self):
#         # Create a request object with an unauthenticated user
#         request = HttpRequest()
#         request.user = AnonymousUser()

#         # Create an instance of the PlanListView
#         view = PlanListView()

#         # Call the dispatch method of the view with the request
#         response = view.dispatch(request)

#         # Assert that the response is a redirect to the login page
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/login/")

#     # Test that the PlanListView returns a list of plans sorted by price
#     def test_plan_list_sorted_by_price(self):
#         # Create test plans with different prices
#         plan1 = Plan.objects.create(name="Plan 1", slug="plan-1", price=100)
#         plan2 = Plan.objects.create(name="Plan 2", slug="plan-2", price=50)
#         plan3 = Plan.objects.create(name="Plan 3", slug="plan-3", price=75)

#         # Make a GET request to the PlanListView
#         response = self.client.get(reverse("plan-list"))

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the plans are sorted by price in descending order
#         plans = response.context["object_list"]
#         self.assertEqual(plans[0], plan1)
#         self.assertEqual(plans[1], plan3)
#         self.assertEqual(plans[2], plan2)

#     # Test that the PlanListView returns a list of plans filtered by name
#     def test_plan_list_view_filter_by_name(self):
#         # Create test plans
#         plan1 = Plan.objects.create(name="Plan 1", slug="plan-1", price=100)
#         plan2 = Plan.objects.create(name="Plan 2", slug="plan-2", price=200)
#         plan3 = Plan.objects.create(name="Plan 3", slug="plan-3", price=300)

#         # Make a GET request to the PlanListView with a filter for 'Plan 2'
#         response = self.client.get("/plans/?name=Plan%202")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that only 'Plan 2' is in the context object
#         self.assertQuerysetEqual(response.context["filter"].qs, ["<Plan: Plan 2>"])

#     # Test that the PlanListView returns a list of plans filtered by features
#     def test_plan_list_view_filter_by_features(self):
#         # Create some plans with different features
#         feature1 = ProductFeature.objects.create(name="Feature 1")
#         feature2 = ProductFeature.objects.create(name="Feature 2")
#         plan1 = Plan.objects.create(name="Plan 1", slug="plan-1", price=100)
#         plan1.features.add(feature1)
#         plan2 = Plan.objects.create(name="Plan 2", slug="plan-2", price=200)
#         plan2.features.add(feature2)
#         plan3 = Plan.objects.create(name="Plan 3", slug="plan-3", price=300)
#         plan3.features.add(feature1, feature2)

#         # Create a request with filter parameters
#         request = self.client.get("/plans/?feature=Feature 1")

#         # Call the view and get the response
#         response = PlanListView.as_view()(request)

#         # Check that the response contains the filtered plans
#         self.assertEqual(response.status_code, 200)
#         self.assertQuerysetEqual(
#             response.context_data["filter"].qs,
#             [repr(plan1), repr(plan3)],
#             ordered=False,
#         )

#     # Test that the PlanListView returns a list of plans filtered by price correctly.
#     def test_plan_list_view_filter_by_price(self):
#         # Create test plans
#         plan1 = Plan.objects.create(name="Plan 1", slug="plan-1", price=100)
#         plan2 = Plan.objects.create(name="Plan 2", slug="plan-2", price=200)
#         plan3 = Plan.objects.create(name="Plan 3", slug="plan-3", price=300)

#         # Make GET request to PlanListView with filter parameter
#         response = self.client.get("/plans/?price__lte=200")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that only plan1 and plan2 are in the response context
#         self.assertIn(plan1, response.context["object_list"])
#         self.assertIn(plan2, response.context["object_list"])
#         self.assertNotIn(plan3, response.context["object_list"])

#     # Test that the PlanListView returns a list of plans filtered by slug
#     def test_plan_list_view_filter_by_slug(self):
#         # Create a plan with a specific slug
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Make a GET request to the PlanListView with the specific slug as a query parameter
#         response = self.client.get("/plans/?slug=test-plan")

#         # Check that the response contains the plan with the specific slug
#         self.assertContains(response, plan.name)
#         self.assertContains(response, plan.slug)
#         self.assertContains(response, plan.description)
#         self.assertContains(response, plan.price)


# class TestCreatePlanView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that a user with admin type can log in and create a plan successfully
#     def test_create_plan_successfully(self):
#         # Create a user with admin type
#         admin_user = User.objects.create(username="admin", type="Admin")

#         # Log in the admin user
#         self.client.force_login(admin_user)

#         # Send a POST request to the CreatePlanView with valid form data
#         response = self.client.post(
#             reverse_lazy("create_plan"),
#             data={"name": "Test Plan", "description": "Test Description", "price": 100},
#         )

#         # Check that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Check that the plan was created successfully
#         self.assertEqual(Plan.objects.count(), 1)
#         plan = Plan.objects.first()
#         self.assertEqual(plan.name, "Test Plan")
#         self.assertEqual(plan.description, "Test Description")
#         self.assertEqual(plan.price, 100)

#         # Check that the user is redirected to the plan list page
#         self.assertRedirects(response, reverse_lazy("plan_list"))

#     # Test that a plan with the minimum required fields is created successfully
#     def test_create_plan_with_minimum_fields(self):
#         # Create a user with admin type
#         admin_user = User.objects.create_user(
#             username="admin", password="admin", type="Admin"
#         )

#         # Log in the admin user
#         self.client.login(username="admin", password="admin")

#         # Send a POST request to the CreatePlanView with the minimum required fields
#         response = self.client.post(
#             reverse_lazy("create_plan"), data={"name": "Basic Plan", "price": 50}
#         )

#         # Check that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Check that a plan with the given name and price is created
#         plan = Plan.objects.get(name="Basic Plan", price=50)
#         self.assertEqual(plan.name, "Basic Plan")
#         self.assertEqual(plan.price, 50)

#     # Test that a plan with all fields filled is created successfully
#     def test_create_plan_successfully(self):
#         # Create a user with type 'Admin'
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )

#         # Log in the admin user
#         self.client.login(username="admin", password="admin123")

#         # Send a POST request to the CreatePlanView with all fields filled
#         response = self.client.post(
#             reverse_lazy("create_plan"),
#             {"name": "Test Plan", "description": "This is a test plan", "price": 100},
#         )

#         # Check that the plan is created successfully
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Plan.objects.count(), 1)
#         plan = Plan.objects.first()
#         self.assertEqual(plan.name, "Test Plan")
#         self.assertEqual(plan.description, "This is a test plan")
#         self.assertEqual(plan.price, 100)

#     # Test that a plan with a duplicate name is not created and an appropriate error message is displayed
#     def test_duplicate_name_not_created(self):
#         # Create a plan with a unique name
#         unique_plan = Plan(
#             name="Unique Plan", description="Unique description", price=100
#         )
#         unique_plan.save()

#         # Create a form with the same name as the unique plan
#         form_data = {
#             "name": "Unique Plan",
#             "description": "Duplicate description",
#             "price": 200,
#         }
#         form = PlanForm(data=form_data)

#         # Check that the form is not valid
#         self.assertFalse(form.is_valid())

#         # Check that the plan is not created
#         self.assertEqual(Plan.objects.count(), 1)

#         # Check that the appropriate error message is displayed
#         self.assertIn("A plan with this name already exists.", form.errors["name"])

#     # Test that when a plan with an invalid price is submitted, it is not created and an appropriate error message is displayed
#     def test_invalid_price_error_message(self):
#         # Create a user with admin privileges
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )

#         # Log in as the admin user
#         self.client.login(username="admin", password="admin123")

#         # Submit a form with an invalid price
#         response = self.client.post(
#             reverse_lazy("create_plan"),
#             data={
#                 "name": "Basic Plan",
#                 "description": "Basic plan description",
#                 "price": "abc",
#             },
#         )

#         # Check that the plan is not created
#         self.assertFalse(Plan.objects.filter(name="Basic Plan").exists())

#         # Check that the appropriate error message is displayed
#         self.assertContains(response, "Enter a valid number.")

#     # Test that a plan with an invalid name is not created and an appropriate error message is displayed
#     def test_invalid_name_not_created(self):
#         # Create a request object
#         request = self.client.post(
#             reverse_lazy("create_plan"), data={"name": "Invalid Name"}
#         )

#         # Check that the plan is not created
#         self.assertFalse(Plan.objects.exists())

#         # Check that the appropriate error message is displayed
#         self.assertContains(request, "Invalid name. Please enter a valid name.")

#     # Test that when a plan with an invalid description is submitted, it is not created and an appropriate error message is displayed
#     def test_invalid_description_error_message(self):
#         # Create a user with admin privileges
#         admin_user = User.objects.create_user(username="admin", password="admin123")
#         admin_user.type = "Admin"
#         admin_user.save()

#         # Log in as the admin user
#         self.client.login(username="admin", password="admin123")

#         # Submit a form with an invalid description
#         response = self.client.post(
#             reverse("create_plan"),
#             data={"name": "Basic Plan", "description": "", "price": 50},
#         )

#         # Check that the plan is not created
#         self.assertFalse(Plan.objects.filter(name="Basic Plan").exists())

#         # Check that the appropriate error message is displayed
#         self.assertContains(response, "Description is required")

#     # Test that a user without admin type is redirected to the permission denied page when trying to create a plan
#     def test_user_without_admin_type_redirected_to_permission_denied_page(self):
#         # Create a user without admin type
#         user = User.objects.create_user(username="testuser", password="testpassword")

#         # Log in the user
#         self.client.login(username="testuser", password="testpassword")

#         # Send a POST request to the create plan view
#         response = self.client.post(
#             reverse_lazy("create_plan"),
#             data={"name": "Test Plan", "description": "Test Description", "price": 100},
#         )

#         # Check that the user is redirected to the permission denied page
#         self.assertEqual(response.status_code, 403)
#         self.assertTemplateUsed(response, "permission_denied.html")

#     # Test that a plan with features is created successfully
#     def test_create_plan_with_features(self):
#         # Create a user with type 'Admin'
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )

#         # Log in the admin user
#         self.client.login(username="admin", password="admin123")

#         # Create a product feature
#         feature = ProductFeature.objects.create(name="Feature 1")

#         # Send a POST request to create a plan with features
#         response = self.client.post(
#             reverse_lazy("create_plan"),
#             data={
#                 "name": "Plan 1",
#                 "description": "Description of Plan 1",
#                 "price": 100,
#                 "features": [feature.id],
#             },
#         )

#         # Check that the plan is created successfully
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Plan.objects.count(), 1)
#         plan = Plan.objects.first()
#         self.assertEqual(plan.name, "Plan 1")
#         self.assertEqual(plan.description, "Description of Plan 1")
#         self.assertEqual(plan.price, 100)
#         self.assertEqual(plan.features.count(), 1)
#         self.assertEqual(plan.features.first().name, "Feature 1")

#     # Test that a plan with a slug is created successfully
#     def test_create_plan_with_slug(self):
#         # Create a plan with a slug
#         plan = Plan(name="Test Plan", description="Test Description", price=100)
#         plan.save()

#         # Check if the plan has a slug
#         self.assertIsNotNone(plan.slug)

#     # Test that the price of a plan is displayed correctly in weekly, quarterly, and annually formats
#     def test_display_price_formats(self):
#         # Create a plan with a price of $100
#         plan = Plan.objects.create(name="Test Plan", price=100)

#         # Check the weekly price
#         self.assertEqual(plan.price_weekly, 25)

#         # Check the quarterly price
#         self.assertEqual(plan.price_quartely, 300)

#         # Check the annually price
#         self.assertEqual(plan.price_annually, 1200)

#     # Test that a plan is not created if the form is invalid and the appropriate error message is displayed
#     def test_invalid_form_error_message(self):
#         # Create a mock request and response
#         request = self.client.post("/create_plan/")
#         response = self.client.get("/create_plan/")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the form is not valid
#         self.assertFalse(response.context["form"].is_valid())

#         # Check that the appropriate error message is displayed
#         self.assertContains(response, "Please correct the errors below.")


# class TestPlanDetailView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that a user with admin type can access the view
#     def test_admin_access(self):
#         # Create a user with admin type
#         admin_user = User.objects.create(username="admin", type="Admin")

#         # Log in the admin user
#         self.client.force_login(admin_user)

#         # Access the PlanDetailView
#         response = self.client.get("/plan/detail/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the correct template is used
#         self.assertTemplateUsed(response, "multitenancy/subscriptions/plan_detail.html")

#         # Check that the model is correctly passed to the template
#         self.assertIsInstance(response.context["object"], Plan)

#     # Test that the Plan object is retrieved and displayed correctly in the PlanDetailView
#     def test_retrieve_and_display_plan_object(self):
#         # Create a Plan object
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Create a request object
#         request = HttpRequest()

#         # Set the user attribute of the request object to an admin user
#         request.user = User(type="Admin")

#         # Create a PlanDetailView object
#         view = PlanDetailView()

#         # Set the request attribute of the view object to the request object
#         view.request = request

#         # Call the get method of the view object
#         response = view.get(request)

#         # Assert that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Assert that the plan object is in the response context
#         self.assertEqual(response.context_data["plan"], plan)

#     # Test that the PlanDetailView class correctly displays the features of a plan
#     def test_plan_features_displayed_correctly(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Basic Plan",
#             slug="basic-plan",
#             description="Basic plan description",
#             price=50,
#         )

#         # Create some product features
#         feature1 = ProductFeature.objects.create(name="Feature 1")
#         feature2 = ProductFeature.objects.create(name="Feature 2")

#         # Add the features to the plan
#         plan.features.add(feature1, feature2)

#         # Get the response from the view
#         response = self.client.get(f"/plan/{plan.slug}")

#         # Check that the features are displayed correctly in the response content
#         self.assertContains(response, "Feature 1")
#         self.assertContains(response, "Feature 2")

#     # Test that the price of a plan is displayed correctly on the PlanDetailView
#     def test_plan_price_displayed_correctly(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Basic Plan",
#             slug="basic-plan",
#             description="Basic plan description",
#             price=100,
#         )

#         # Create a request object
#         request = HttpRequest()

#         # Create an instance of PlanDetailView
#         view = PlanDetailView()
#         view.setup(request)

#         # Set the object attribute of the view to the created plan
#         view.object = plan

#         # Get the context data from the view
#         context = view.get_context_data()

#         # Check that the price is displayed correctly in the context data
#         self.assertEqual(context["object"].price, 100)

#     # Test that the price weekly of a plan is displayed correctly in the PlanDetailView
#     def test_plan_price_weekly_displayed_correctly(self):
#         # Create a plan with a price of 100
#         plan = Plan.objects.create(name="Test Plan", slug="test-plan", price=100)

#         # Create a request object
#         request = HttpRequest()

#         # Set the user type to 'Admin'
#         request.user = User(type="Admin")

#         # Create an instance of PlanDetailView
#         view = PlanDetailView()

#         # Set the request object for the view
#         view.request = request

#         # Set the plan object for the view
#         view.object = plan

#         # Get the price weekly from the view
#         price_weekly = view.object.price_weekly

#         # Assert that the price weekly is equal to 25 (100 / 4)
#         self.assertEqual(price_weekly, 25)

#     # Test that the price quarterly is displayed correctly on the PlanDetailView
#     def test_plan_price_quarterly_displayed_correctly(self):
#         # Create a Plan object
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Get the PlanDetailView
#         view = PlanDetailView()

#         # Set the request user as an admin
#         view.request = RequestFactory().get("/")
#         view.request.user = User.objects.create(username="admin", type="Admin")

#         # Set the object attribute of the view to the created Plan object
#         view.object = plan

#         # Get the price quarterly from the view
#         price_quarterly = view.object.price_quartely

#         # Assert that the price quarterly is equal to the expected value
#         self.assertEqual(price_quarterly, 300)

#     # Test that the price_annually property of PlanDetailView displays the correct price
#     def test_display_price_annually(self):
#         # Create a Plan object with a specific price
#         plan = Plan(name="Test Plan", slug="test-plan", price=100)
#         plan.save()

#         # Create a request object with an admin user
#         request = RequestFactory().get("/")
#         request.user = User(type="Admin")

#         # Create an instance of PlanDetailView
#         view = PlanDetailView()
#         view.setup(request)

#         # Set the model object of the view to the created Plan object
#         view.object = plan

#         # Call the price_annually property and check if it returns the correct price
#         self.assertEqual(view.price_annually, 1200)

#     # Test that a user without admin type cannot access the view
#     def test_user_without_admin_cannot_access_view(self):
#         # Create a user without admin type
#         user = User.objects.create(username="testuser", type="User")
#         user.set_password("testpassword")
#         user.save()

#         # Log in the user
#         self.client.login(username="testuser", password="testpassword")

#         # Access the view
#         response = self.client.get("/plan/detail/")

#         # Assert that the response status code is 403 Forbidden
#         self.assertEqual(response.status_code, 403)

#     # Test that a plan with no features is displayed correctly in the PlanDetailView
#     def test_no_features_displayed_correctly(self):
#         # Create a plan with no features
#         plan = Plan.objects.create(
#             name="Basic Plan",
#             slug="basic-plan",
#             description="This is a basic plan",
#             price=50,
#         )

#         # Make a GET request to the PlanDetailView
#         response = self.client.get(f"/plan/{plan.slug}")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the plan name is displayed correctly in the response content
#         self.assertContains(response, plan.name)

#         # Check that the plan description is displayed correctly in the response content
#         self.assertContains(response, plan.description)

#         # Check that the plan price is displayed correctly in the response content
#         self.assertContains(response, f"${plan.price}")

#         # Check that the plan features are not displayed in the response content
#         self.assertNotContains(response, "Features")

#     # Test that the PlanDetailView correctly displays a plan with no description
#     def test_plan_with_no_description_displayed_correctly(self):
#         # Create a plan with no description
#         plan = Plan.objects.create(name="Basic Plan", slug="basic-plan", price=50)

#         # Create a request object
#         request = HttpRequest()

#         # Set the user type to 'Admin'
#         request.user = User(type="Admin")

#         # Create an instance of PlanDetailView
#         view = PlanDetailView()

#         # Set the request object for the view
#         view.request = request

#         # Set the kwargs for the view
#         view.kwargs = {"pk": plan.pk}

#         # Call the get method of the view
#         response = view.get(request)

#         # Assert that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Assert that the plan name is displayed correctly in the response content
#         self.assertIn(plan.name, response.content.decode())

#         # Assert that the plan description is not displayed in the response content
#         self.assertNotIn(plan.description, response.content.decode())

#     # Test that the save method of PlanDetailView adds a slug if it is not present
#     def test_save_method_with_no_slug(self):
#         plan = Plan(name="Test Plan", description="Test Description", price=100)
#         plan.save()
#         self.assertIsNotNone(plan.slug)

#     # Test that a plan with a name that already exists cannot be saved
#     def test_save_plan_with_existing_name(self):
#         # Create a plan with a name that already exists
#         existing_plan = Plan.objects.create(name="Existing Plan", slug="existing-plan")

#         # Create a new plan with the same name
#         new_plan = Plan(name="Existing Plan", slug="new-plan")

#         # Try to save the new plan
#         with self.assertRaises(IntegrityError):
#             new_plan.save()

#     # Test that a plan with a blank name cannot be saved
#     def test_blank_name_cannot_be_saved(self):
#         plan = Plan(name="", slug="test-plan", description="Test plan", price=100)
#         with self.assertRaises(ValidationError):
#             plan.full_clean()

#     # Test that a Plan with a new feature can be saved correctly
#     def test_save_plan_with_new_feature(self):
#         # Create a new Plan
#         plan = Plan(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )
#         plan.save()

#         # Add a new feature to the Plan
#         plan.add_feature("New Feature")

#         # Check if the feature was added correctly
#         self.assertEqual(plan.features.count(), 1)
#         self.assertEqual(plan.features.first().name, "New Feature")

#     # Test that a Plan with a new name can be saved correctly
#     def test_save_plan_with_new_name(self):
#         # Create a new Plan object
#         plan = Plan(
#             name="New Plan",
#             slug="new-plan",
#             description="New plan description",
#             price=100,
#         )

#         # Save the Plan object
#         plan.save()

#         # Retrieve the saved Plan object from the database
#         saved_plan = Plan.objects.get(slug="new-plan")

#         # Check if the name of the saved Plan object is correct
#         self.assertEqual(saved_plan.name, "New Plan")

#     # Test that a Plan with a new price can be saved correctly
#     def test_save_plan_with_new_price(self):
#         # Create a new Plan
#         plan = Plan(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )
#         plan.save()

#         # Update the price of the Plan
#         plan.price = 200
#         plan.save()

#         # Retrieve the updated Plan from the database
#         updated_plan = Plan.objects.get(slug="test-plan")

#         # Check if the price of the updated Plan is correct
#         self.assertEqual(updated_plan.price, 200)

#     # Test that a Plan object with a new description can be saved correctly
#     def test_save_plan_with_new_description(self):
#         # Create a Plan object
#         plan = Plan(name="Test Plan", slug="test-plan", description="Old Description")
#         plan.save()

#         # Update the description
#         plan.description = "New Description"
#         plan.save()

#         # Retrieve the updated Plan object from the database
#         updated_plan = Plan.objects.get(slug="test-plan")

#         # Check if the description is updated correctly
#         self.assertEqual(updated_plan.description, "New Description")

#     # Test that a Plan with a new slug can be saved correctly
#     def test_save_plan_with_new_slug(self):
#         # Create a new Plan object
#         plan = Plan(name="Test Plan", description="Test Description", price=100)
#         plan.save()

#         # Check if the slug is generated correctly
#         self.assertEqual(plan.slug, "test-plan")

#         # Check if the Plan is saved correctly
#         saved_plan = Plan.objects.get(slug="test-plan")
#         self.assertEqual(saved_plan.name, "Test Plan")
#         self.assertEqual(saved_plan.description, "Test Description")
#         self.assertEqual(saved_plan.price, 100)


# class TestFeatureCreateView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that when the form is valid, a feature is created and added to the plan's features
#     def test_valid_form_feature_created_and_added_to_plan(self):
#         # Create a mock request object
#         request = MagicMock()
#         request.method = "POST"
#         request.content_params = {}

#         # Create a mock form object
#         form = MagicMock()
#         form.is_valid.return_value = True
#         form.cleaned_data = {
#             "name": "Test Feature",
#             "description": "Test Description",
#             "plan_name": "Test Plan",
#             "plan": 1,
#         }

#         # Create a mock feature object
#         feature = MagicMock()
#         feature.pk = 1

#         # Create a mock plan object
#         plan = MagicMock()
#         plan.features = MagicMock()
#         plan.features.add.return_value = None

#         # Patch the necessary objects
#         with patch("django.shortcuts.render") as mock_render, patch(
#             "sweetify.success"
#         ) as mock_success, patch(
#             "django.http.HttpResponseRedirect"
#         ) as mock_redirect, patch(
#             "multitenancy.subscriptions.views.ProductFeatureForm", return_value=form
#         ), patch(
#             "multitenancy.subscriptions.views.ProductFeature.objects.create",
#             return_value=feature,
#         ), patch(
#             "multitenancy.subscriptions.views.Plan.objects.get", return_value=plan
#         ):

#             # Create an instance of FeatureCreateView
#             view = FeatureCreateView()

#             # Call the post method with the mock request object
#             response = view.post(request)

#             # Assert that the necessary methods were called with the correct arguments
#             form.is_valid.assert_called_once()
#             form.cleaned_data.assert_called_once_with()
#             ProductFeature.objects.create.assert_called_once_with(
#                 name="Test Feature", description="Test Description"
#             )
#             plan.features.add.assert_called_once_with(feature)
#             sweetify.success.assert_called_once_with(
#                 request, "Successfully Added Feature!", icon="success", timer=5000
#             )
#             mock_redirect.assert_called_once_with("/admin/settings/plans/Test Plan/")
#             mock_render.assert_not_called()

#             # Assert that the response is an instance of HttpResponseRedirect
#             self.assertIsInstance(response, HttpResponseRedirect)

#     # Test that when the form is invalid, it is rendered with errors
#     def test_form_invalid_render_errors(self):
#         # Create a mock request object
#         request = HttpRequest()
#         request.method = "POST"
#         request.POST = {
#             "name": "Test Feature",
#             "description": "Test Description",
#             "plan_name": "Test Plan",
#             "plan": 1,
#         }

#         # Create an instance of the FeatureCreateView class
#         view = FeatureCreateView()

#         # Call the post method of the view with the mock request object
#         response = view.post(request)

#         # Assert that the response is an instance of the render function
#         self.assertIsInstance(response, render)

#         # Assert that the response contains the form with errors
#         self.assertIn("form", response.context)
#         self.assertTrue(response.context["form"].errors)

#     # Test that when the plan does not exist, the user is redirected to the plan detail page with an error message
#     def test_plan_not_exist_redirect(self):
#         # Create a mock request object
#         request = HttpRequest()
#         request.method = "POST"
#         request.POST = {
#             "name": "Feature 1",
#             "description": "This is a feature",
#             "plan_name": "Plan 1",
#             "plan": 1,
#         }

#         # Create a mock form object
#         form = ProductFeatureForm(request.POST)
#         form.is_valid = MagicMock(return_value=True)
#         form.cleaned_data = {
#             "name": "Feature 1",
#             "description": "This is a feature",
#             "plan_name": "Plan 1",
#             "plan": 1,
#         }

#         # Create a mock feature object
#         feature = ProductFeature(name="Feature 1", description="This is a feature")
#         feature.save = MagicMock()

#         # Create a mock plan object
#         plan = Plan(name="Plan 1", slug="plan-1", description="This is a plan")
#         plan.save = MagicMock()
#         plan.features.add = MagicMock()

#         # Mock the get method of Plan.objects
#         Plan.objects.get = MagicMock(side_effect=Plan.DoesNotExist)

#         # Create a mock sweetify object
#         sweetify.success = MagicMock()
#         sweetify.error = MagicMock()

#         # Create a mock render function
#         render = MagicMock()

#         # Create an instance of FeatureCreateView
#         view = FeatureCreateView()

#         # Call the post method of FeatureCreateView
#         response = view.post(request)

#         # Assert that the user is redirected to the plan detail page
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/admin/settings/plans/Plan 1/")

#         # Assert that the error message is displayed
#         sweetify.error.assert_called_with(request, "Failed to Add Feature!")

#         # Assert that the form is rendered with the errors
#         render.assert_called_with(
#             request,
#             "multitenancy/subscriptions/plan_detail.html",
#             {"feature_form": form},
#         )

#     # Test that when the feature creation fails, the user is redirected to the plan detail page with an error message
#     def test_feature_creation_fails(self):
#         # Create a mock request object
#         request = MagicMock()
#         request.method = "POST"
#         request.content_params = {}

#         # Create a mock form object
#         form = MagicMock()
#         form.is_valid.return_value = False

#         # Create a mock ProductFeatureForm object
#         ProductFeatureForm = MagicMock(return_value=form)

#         # Create a mock Plan object
#         plan = MagicMock()
#         plan.name = "Test Plan"

#         # Create a mock ProductFeature object
#         feature = MagicMock()
#         feature.pk = 1

#         # Create a mock Plan.objects.get() method
#         Plan.objects.get.return_value = plan

#         # Create a mock ProductFeature.objects.create() method
#         ProductFeature.objects.create.return_value = feature

#         # Create a mock sweetify.success() method
#         sweetify.success = MagicMock()

#         # Create a mock sweetify.error() method
#         sweetify.error = MagicMock()

#         # Create a mock HttpResponseRedirect object
#         HttpResponseRedirect = MagicMock()

#         # Create an instance of FeatureCreateView
#         view = FeatureCreateView()

#         # Set the request attribute of the view to the mock request object
#         view.request = request

#         # Set the form_class attribute of the view to the mock ProductFeatureForm object
#         view.form_class = ProductFeatureForm

#         # Set the success_url attribute of the view to "/admin/settings/plans/{plan_name}/"
#         view.success_url = "/admin/settings/plans/{plan_name}/"

#         # Call the post() method of the view
#         response = view.post(request)

#         # Assert that the form_class was called with the request.POST data
#         ProductFeatureForm.assert_called_with(request.POST)

#         # Assert that the form.is_valid() method was called
#         form.is_valid.assert_called()

#         # Assert that the sweetify.error() method was called with the request object and the error message
#         sweetify.error.assert_called_with(request, "Failed to Add Feature!")

#         # Assert that the HttpResponseRedirect was called with the correct URL
#         HttpResponseRedirect.assert_called_with("/admin/settings/plans/{plan_name}/")

#         # Assert that the response is equal to the HttpResponseRedirect
#         self.assertEqual(response, HttpResponseRedirect)

#     # Test that when the plan name and plan id do not match, the view redirects to the plan detail page with an error message
#     def test_plan_name_and_id_mismatch(self):
#         # Create a mock request object
#         request = self.client.post(
#             "/admin/feature/create/",
#             {
#                 "name": "Test Feature",
#                 "description": "Test Description",
#                 "plan": 1,
#                 "plan_name": "Mismatched Plan",
#             },
#         )

#         # Assert that the response is a redirect
#         self.assertEqual(request.status_code, 302)

#         # Assert that the redirect is to the plan detail page
#         self.assertEqual(request.url, "/admin/settings/plans/Mismatched Plan/")

#         # Assert that the error message is displayed
#         self.assertContains(request, "Failed to Add Feature!")

#     # Test that when the form is not submitted via POST method, the view redirects to the plan detail page with an error message
#     def test_redirect_to_plan_detail_page_with_error_message(self):
#         # Create a mock request object
#         request = MagicMock()
#         request.method = "GET"

#         # Create an instance of FeatureCreateView
#         view = FeatureCreateView()

#         # Call the post method of the view
#         response = view.post(request)

#         # Assert that the response is an instance of HttpResponseRedirect
#         self.assertIsInstance(response, HttpResponseRedirect)

#         # Assert that the response redirects to the plan detail page
#         self.assertEqual(response.url, "/admin/settings/plans/{plan_name}/")

#         # Assert that the sweetify.error function is called
#         sweetify.error.assert_called_once_with(request, "Failed to Add Feature!")

#     # Test that when a user is not logged in, the view redirects to the login page
#     def test_redirect_to_login_page(self):
#         # Create a request object without a logged in user
#         request = HttpRequest()

#         # Create an instance of the FeatureCreateView class
#         view = FeatureCreateView()

#         # Call the post method of the view with the request object
#         response = view.post(request)

#         # Assert that the response is an instance of HttpResponseRedirect
#         self.assertIsInstance(response, HttpResponseRedirect)

#         # Assert that the response redirects to the login page
#         self.assertEqual(response.url, "/login/")

#     # Test that when the user is not an admin, the view redirects to the permission denied page.
#     def test_user_not_admin_redirect_permission_denied(self):
#         # Create a mock request object with a non-admin user
#         request = HttpRequest()
#         request.user = User(type="User")

#         # Create an instance of FeatureCreateView
#         view = FeatureCreateView()

#         # Call the post method of the view with the mock request
#         response = view.post(request)

#         # Assert that the response is an instance of HttpResponseRedirect
#         self.assertIsInstance(response, HttpResponseRedirect)

#         # Assert that the response redirects to the permission denied page
#         self.assertEqual(response.url, "/permission-denied/")

#     # Test that a feature is successfully created when the feature name and description are at their maximum length, the form is valid, and the feature is added to the plan
#     def test_feature_creation_with_maximum_length(self):
#         # Create a request object
#         request = HttpRequest()
#         request.method = "POST"
#         request.POST = {
#             "name": "A" * 250,
#             "description": "B" * 250,
#             "plan_name": "Test Plan",
#             "plan": 1,
#         }

#         # Create an instance of the FeatureCreateView class
#         view = FeatureCreateView()

#         # Call the post method of the view with the request object
#         response = view.post(request)

#         # Assert that the feature was successfully created and added to the plan
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/admin/settings/plans/Test Plan/")
#         self.assertEqual(ProductFeature.objects.count(), 1)
#         self.assertEqual(Plan.objects.first().features.count(), 1)

#     # Test that when the feature name and description are empty, the form is invalid and the form is rendered with errors
#     def test_empty_name_and_description(self):
#         # Create a request object
#         request = HttpRequest()
#         request.method = "POST"
#         request.POST = {
#             "name": "",
#             "description": "",
#             "plan": 1,
#             "plan_name": "Test Plan",
#         }

#         # Create an instance of the FeatureCreateView class
#         view = FeatureCreateView()

#         # Call the post method of the view with the request object
#         response = view.post(request)

#         # Assert that the response is a redirect
#         self.assertIsInstance(response, HttpResponseRedirect)

#         # Assert that the redirect URL is correct
#         self.assertEqual(response.url, "/admin/settings/plans/Test Plan/")

#         # Assert that the sweetify.error method was called
#         self.assertTrue(sweetify.error.called)

#         # Assert that the form is rendered with errors
#         self.assertContains(response, "This field is required")


# class TestUpdatePlanView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()


#     # Test that the UpdatePlanView updates the plan successfully with new features added when the user is authenticated as an admin and the form is valid.
#     def test_update_plan_with_new_features(self):
#         # Create a user with admin privileges
#         admin_user = User.objects.create(username="admin", type="Admin")
#         admin_user.set_password("admin")
#         admin_user.save()

#         # Log in the admin user
#         self.client.login(username="admin", password="admin")

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Basic", slug="basic", description="Basic plan", price=50
#         )

#         # Create a product feature
#         feature = ProductFeature.objects.create(name="Feature 1")

#         # Add the feature to the plan
#         plan.features.add(feature)

#         # Create a form with updated plan data
#         form_data = {
#             "name": "Premium",
#             "description": "Premium plan",
#             "price": 100,
#             "features": ["Feature 1", "Feature 2"],
#         }
#         form = PlanForm(data=form_data, instance=plan)

#         # Submit the form
#         response = self.client.post(
#             reverse_lazy("update_plan", kwargs={"pk": plan.pk}), data=form_data
#         )

#         # Check that the plan is updated successfully
#         self.assertEqual(response.status_code, 302)
#         updated_plan = Plan.objects.get(pk=plan.pk)
#         self.assertEqual(updated_plan.name, "Premium")
#         self.assertEqual(updated_plan.description, "Premium plan")
#         self.assertEqual(updated_plan.price, 100)
#         self.assertEqual(updated_plan.features.count(), 2)
#         self.assertTrue(updated_plan.features.filter(name="Feature 1").exists())
#         self.assertTrue(updated_plan.features.filter(name="Feature 2").exists())
#         self.assertFalse(updated_plan.features.filter(name="Feature 3").exists())
#         self.assertEqual(updated_plan.price_weekly, 25)
#         self.assertEqual(updated_plan.price_quartely, 300)
#         self.assertEqual(updated_plan.price_annually, 1200)

#     # Test that the UpdatePlanView updates the plan successfully with a new slug when the user is authenticated as an admin and the form is valid.
#     def test_update_plan_successfully(self):
#         # Create a user with admin privileges
#         admin_user = User.objects.create(username="admin", type="Admin")
#         admin_user.set_password("admin")
#         admin_user.save()

#         # Log in the admin user
#         self.client.login(username="admin", password="admin")

#         # Create a plan
#         plan = Plan.objects.create(name="Basic", description="Basic plan", price=50)

#         # Send a POST request to update the plan
#         response = self.client.post(
#             reverse_lazy("update_plan", kwargs={"pk": plan.pk}),
#             data={"name": "Premium", "description": "Premium plan", "price": 100},
#         )

#         # Check that the plan was updated successfully
#         self.assertEqual(response.status_code, 302)
#         updated_plan = Plan.objects.get(pk=plan.pk)
#         self.assertEqual(updated_plan.name, "Premium")
#         self.assertEqual(updated_plan.description, "Premium plan")
#         self.assertEqual(updated_plan.price, 100)
#         self.assertEqual(updated_plan.slug, "premium")


#     # Test that when a user is not authenticated, they are redirected to the login page
#     def test_redirect_to_login_page(self):
#         # Create a request object without an authenticated user
#         request = RequestFactory().get("/update-plan/1")
#         request.user = AnonymousUser()

#         # Create an instance of the UpdatePlanView class
#         view = UpdatePlanView()

#         # Call the dispatch method of the view
#         response = view.dispatch(request, pk=1)

#         # Assert that the response is a redirect to the login page
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/login/")

#     # Test that when a user is authenticated but not an admin, they are redirected to the permission denied page
#     def test_redirect_permission_denied(self):
#         # Create a non-admin user
#         user = User.objects.create_user(username="testuser", password="testpassword")

#         # Log in the user
#         self.client.login(username="testuser", password="testpassword")

#         # Send a GET request to the UpdatePlanView
#         response = self.client.get(reverse("update_plan", kwargs={"pk": 1}))

#         # Check that the response status code is 403 (Forbidden)
#         self.assertEqual(response.status_code, 403)

#         # Check that the response contains the permission denied message
#         self.assertContains(response, "Permission Denied")

#     # Test that when the form is not valid, the view returns form errors
#     def test_form_not_valid(self):
#         # Create a mock request object
#         request = RequestFactory().get("/")

#         # Create an instance of the view
#         view = UpdatePlanView()

#         # Set the request object on the view
#         view.request = request

#         # Call the get method on the view
#         response = view.get(request)

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Assert that the response contains the form errors
#         self.assertContains(response, "Form is not valid")

#     # Test that when the plan name already exists, the form returns errors
#     def test_plan_name_already_exists(self):
#         # Create a plan with a specific name
#         existing_plan = Plan.objects.create(
#             name="Existing Plan", slug="existing-plan", price=100
#         )

#         # Create a request object with the necessary data
#         request = self.client.post(
#             reverse_lazy("update_plan", kwargs={"pk": existing_plan.pk}),
#             data={"name": "Existing Plan"},
#         )

#         # Check that the form returns errors
#         self.assertFormError(
#             request, "form", "name", "Plan with this Name already exists."
#         )

#     # Test that when the slug is not unique, the form returns errors
#     def test_slug_not_unique(self):
#         # Create a plan with a non-unique slug
#         plan = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Description", price=100
#         )

#         # Create a form with the same slug
#         form_data = {
#             "name": "Plan 2",
#             "slug": "plan-1",
#             "description": "Description",
#             "price": 200,
#         }
#         form = PlanForm(data=form_data)

#         # Assert that the form is not valid and contains errors
#         self.assertFalse(form.is_valid())
#         self.assertIn("slug", form.errors)

#     # Test that the features of a plan are updated successfully
#     def test_update_plan_features(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Basic", slug="basic", description="Basic plan", price=50
#         )

#         # Create product features
#         feature1 = ProductFeature.objects.create(name="Feature 1")
#         feature2 = ProductFeature.objects.create(name="Feature 2")

#         # Add features to the plan
#         plan.features.add(feature1)
#         plan.features.add(feature2)

#         # Update the plan features
#         new_feature1 = ProductFeature.objects.create(name="New Feature 1")
#         new_feature2 = ProductFeature.objects.create(name="New Feature 2")
#         data = {
#             "name": "Basic",
#             "slug": "basic",
#             "description": "Basic plan",
#             "price": 50,
#             "features": [new_feature1.id, new_feature2.id],
#         }
#         form = PlanForm(data=data, instance=plan)
#         self.assertTrue(form.is_valid())
#         form.save()

#         # Retrieve the updated plan
#         updated_plan = Plan.objects.get(id=plan.id)

#         # Check if the features are updated correctly
#         self.assertEqual(updated_plan.features.count(), 2)
#         self.assertIn(new_feature1, updated_plan.features.all())
#         self.assertIn(new_feature2, updated_plan.features.all())

#     # Test that the price_weekly property of a Plan instance is calculated correctly
#     def test_calculate_price_weekly(self):
#         # Create a Plan instance with a price of 100
#         plan = Plan(price=100)

#         # Calculate the expected price weekly
#         expected_price_weekly = 100 / 4

#         # Check if the calculated price weekly matches the expected price weekly
#         self.assertEqual(plan.price_weekly, expected_price_weekly)

#     # Test that the price_quartely property of the Plan model calculates the quarterly price correctly
#     def test_calculate_price_quarterly(self):
#         # Create a Plan instance with a specific price
#         plan = Plan(price=100)

#         # Calculate the expected quarterly price
#         expected_price_quarterly = plan.price * 3

#         # Check if the calculated quarterly price matches the expected price
#         self.assertEqual(plan.price_quartely, expected_price_quarterly)

#     # Test that the price_annually property of the Plan model calculates the correct price by multiplying the monthly price by 12.
#     def test_calculate_price_annually(self):
#         plan = Plan(name="Test Plan", price=100)
#         price_annually = plan.price_annually
#         expected_price_annually = 1200
#         self.assertEqual(price_annually, expected_price_annually)

#     # Test that the plan is deleted successfully when the delete action is performed.
#     def test_delete_plan_successfully(self):
#         # Create a plan object
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Make a DELETE request to the UpdatePlanView with the plan's ID
#         response = self.client.delete(
#             reverse_lazy("update_plan", kwargs={"pk": plan.pk}),
#             urlconf="multitenancy.urls",
#         )

#         # Check that the plan is deleted from the database
#         self.assertFalse(Plan.objects.filter(pk=plan.pk).exists())

#         # Check that the response has a 302 status code, indicating a successful redirect
#         self.assertEqual(response.status_code, 302)

#         # Check that the response redirects to the 'plan_list' URL
#         self.assertEqual(
#             response.url, reverse_lazy("plan_list", urlconf="multitenancy.urls")
#         )

#     # Test that the UpdatePlanView returns a 404 error when the requested plan is not found
#     def test_plan_not_found(self):
#         # Create a mock request object
#         request = self.client.get("/path/to/nonexistent/plan/")

#         # Call the UpdatePlanView with the mock request
#         response = UpdatePlanView.as_view()(request)

#         # Assert that the response status code is 404
#         self.assertEqual(response.status_code, 404)


# class TestDeletePlanView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that a logged in admin user can successfully delete a plan.
#     def test_delete_plan_successfully(self):
#         # Create a logged in admin user
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )
#         self.client.login(username="admin", password="admin123")

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Plan 1 description", price=100
#         )

#         # Send a delete request for the plan
#         response = self.client.post(
#             reverse_lazy("delete_plan", kwargs={"pk": plan.pk}), follow=True
#         )

#         # Check that the plan is deleted
#         self.assertFalse(Plan.objects.filter(pk=plan.pk).exists())

#         # Check that the response is successful
#         self.assertEqual(response.status_code, 200)

#         # Check that the user is redirected to the plan list page
#         self.assertRedirects(
#             response, reverse_lazy("plan_list", urlconf="multitenancy.urls")
#         )

#     # Test that an authenticated admin user cannot delete a plan that does not exist.
#     def test_delete_nonexistent_plan_as_admin(self):
#         # Create an authenticated admin user
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )
#         self.client.login(username="admin", password="admin123")

#         # Attempt to delete a nonexistent plan
#         response = self.client.post(
#             reverse_lazy("delete_plan", kwargs={"pk": 999}), follow=True
#         )

#         # Assert that the response status code is 404 (Not Found)
#         self.assertEqual(response.status_code, 404)

#         # Assert that the plan was not deleted
#         self.assertEqual(Plan.objects.count(), 0)

#     # Test that an authenticated admin user cannot delete a plan that is already deleted.
#     def test_delete_already_deleted_plan(self):
#         # Create an admin user
#         admin_user = User.objects.create(username="admin", type="Admin")
#         admin_user.set_password("admin")
#         admin_user.save()

#         # Log in as the admin user
#         self.client.login(username="admin", password="admin")

#         # Create a plan
#         plan = Plan.objects.create(name="Test Plan", slug="test-plan")

#         # Delete the plan
#         plan.delete()

#         # Try to delete the already deleted plan
#         response = self.client.post(reverse_lazy("delete_plan", kwargs={"pk": plan.pk}))

#         # Assert that the response status code is 404 (Not Found)
#         self.assertEqual(response.status_code, 404)

#         # Assert that the plan is still deleted
#         self.assertFalse(Plan.objects.filter(pk=plan.pk).exists())

#     # Test that an unauthenticated user is unable to delete a plan.
#     def test_unauthenticated_user_deletes_plan(self):
#         # Create an instance of DeletePlanView
#         view = DeletePlanView()

#         # Create a mock request object with an unauthenticated user
#         request = RequestFactory().get("/delete-plan")
#         request.user = AnonymousUser()

#         # Call the get method of DeletePlanView
#         response = view.get(request)

#         # Assert that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Assert that the user is redirected to the login page
#         self.assertEqual(response.url, "/login/?next=/delete-plan")

#         # Assert that the plan is not deleted
#         self.assertEqual(Plan.objects.count(), 1)

#     # Test that a non-admin user is unable to delete a plan
#     def test_non_admin_user_delete_plan(self):
#         # Create a non-admin user
#         user = User.objects.create(username="testuser", type="Non-Admin")
#         # Login the user
#         self.client.force_login(user)

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Send a delete request for the plan
#         response = self.client.delete(reverse("delete_plan", kwargs={"pk": plan.pk}))

#         # Assert that the response status code is 403 Forbidden
#         self.assertEqual(response.status_code, 403)

#         # Assert that the plan still exists in the database
#         self.assertTrue(Plan.objects.filter(pk=plan.pk).exists())

#     # Test that when an authenticated admin user tries to delete a plan with invalid data, the plan is not deleted and the user is redirected to the plan list page.
#     def test_delete_plan_with_invalid_data(self):
#         # Create an authenticated admin user
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )
#         self.client.login(username="admin", password="admin123")

#         # Create a plan with invalid data
#         plan = Plan.objects.create(
#             name="", slug="invalid-plan", description="Invalid plan"
#         )

#         # Send a delete request for the plan
#         response = self.client.post(
#             reverse_lazy("delete_plan", kwargs={"pk": plan.pk}), follow=True
#         )

#         # Assert that the plan is not deleted
#         self.assertTrue(Plan.objects.filter(pk=plan.pk).exists())

#         # Assert that the user is redirected to the plan list page
#         self.assertRedirects(
#             response, reverse_lazy("plan_list", urlconf="multitenancy.urls")
#         )

#     # Test that an authenticated admin user is unable to delete a plan that has associated data.
#     def test_delete_plan_with_associated_data(self):
#         # Create an admin user
#         admin_user = User.objects.create_user(
#             username="admin", password="admin123", type="Admin"
#         )

#         # Create a plan with associated data
#         plan = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Plan 1 description"
#         )
#         feature = ProductFeature.objects.create(name="Feature 1")
#         plan.features.add(feature)
#         plan.save()

#         # Login as admin user
#         self.client.login(username="admin", password="admin123")

#         # Attempt to delete the plan
#         response = self.client.post(reverse("delete_plan", kwargs={"pk": plan.pk}))

#         # Assert that the plan was not deleted
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "multitenancy/subscriptions/delete_plan.html")
#         self.assertContains(
#             response, "This plan cannot be deleted because it has associated data."
#         )

#     # Test that when a user is authenticated as an admin and cancels the deletion of a plan, the plan is not deleted.
#     def test_cancel_deletion_as_admin(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Authenticate as an admin
#         self.client.login(username="admin", password="adminpassword")

#         # Send a POST request to cancel the deletion of the plan
#         response = self.client.post(
#             reverse_lazy("delete_plan", kwargs={"pk": plan.pk}), data={"cancel": True}
#         )

#         # Assert that the plan is not deleted
#         self.assertEqual(Plan.objects.filter(pk=plan.pk).exists(), True)

#         # Assert that the response status code is 302 (redirect)
#         self.assertEqual(response.status_code, 302)

#         # Assert that the user is redirected to the plan list page
#         self.assertEqual(
#             response.url, reverse_lazy("plan_list", urlconf="multitenancy.urls")
#         )

#     # Test that an authenticated admin user is unable to delete a plan while another admin user is editing it.
#     def test_delete_plan_while_another_admin_editing(self):
#         # Create two admin users
#         admin1 = User.objects.create(username="admin1", type="Admin")
#         admin2 = User.objects.create(username="admin2", type="Admin")

#         # Log in admin1
#         self.client.force_login(admin1)

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan", slug="test-plan", description="Test Description"
#         )

#         # Log in admin2
#         self.client.force_login(admin2)

#         # Edit the plan
#         response = self.client.get(reverse("edit_plan", kwargs={"pk": plan.pk}))

#         # Check that the response is successful
#         self.assertEqual(response.status_code, 200)

#         # Log in admin1 again
#         self.client.force_login(admin1)

#         # Try to delete the plan
#         response = self.client.post(reverse("delete_plan", kwargs={"pk": plan.pk}))

#         # Check that the response is forbidden
#         self.assertEqual(response.status_code, 403)

#         # Check that the plan still exists
#         self.assertTrue(Plan.objects.filter(pk=plan.pk).exists())

#     # Test that when a user is authenticated as an admin and tries to delete a plan while another admin is deleting it, the user is not able to delete the plan and receives an appropriate error message.
#     def test_delete_plan_while_another_admin_deleting(self):
#         # Create two admin users
#         admin1 = User.objects.create(username="admin1", type="Admin")
#         admin2 = User.objects.create(username="admin2", type="Admin")

#         # Authenticate admin1
#         self.client.force_login(admin1)

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan", slug="test-plan", description="Test Description"
#         )

#         # Set the plan being deleted by admin2
#         plan.being_deleted_by = admin2
#         plan.save()

#         # Try to delete the plan
#         response = self.client.post(reverse("delete_plan", kwargs={"pk": plan.pk}))

#         # Assert that the plan was not deleted
#         self.assertEqual(Plan.objects.filter(pk=plan.pk).exists(), True)

#         # Assert that the user received an appropriate error message
#         self.assertContains(
#             response,
#             "Another admin is currently deleting this plan. Please try again later.",
#         )

#     # Test that an admin user is unable to delete a plan while another user is editing it
#     def test_delete_plan_while_another_user_editing(self):
#         # Create an admin user
#         admin_user = User.objects.create(username="admin", type="Admin")
#         admin_user.set_password("admin123")
#         admin_user.save()

#         # Create a regular user
#         regular_user = User.objects.create(username="regular", type="Regular")
#         regular_user.set_password("regular123")
#         regular_user.save()

#         # Log in as the admin user
#         self.client.login(username="admin", password="admin123")

#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan", slug="test-plan", description="Test Description"
#         )

#         # Log in as the regular user
#         self.client.login(username="regular", password="regular123")

#         # Edit the plan
#         response = self.client.get(reverse_lazy("edit_plan", kwargs={"pk": plan.pk}))

#         # Log in as the admin user again
#         self.client.login(username="admin", password="admin123")

#         # Attempt to delete the plan
#         response = self.client.post(reverse_lazy("delete_plan", kwargs={"pk": plan.pk}))

#         # Assert that the plan was not deleted
#         self.assertEqual(response.status_code, 403)
#         self.assertTrue(Plan.objects.filter(pk=plan.pk).exists())


# class TestSubscriptionsListView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the 'subscriptions_list.html' template is rendered correctly
#     def test_render_subscriptions_list_template(self):
#         # Create a request object
#         request = HttpRequest()

#         # Create a user object with type 'Admin'
#         user = User(type="Admin")

#         # Set the user as the authenticated user in the request
#         request.user = user

#         # Create an instance of SubscriptionsListView
#         view = SubscriptionsListView()

#         # Set the request in the view
#         view.request = request

#         # Call the get method of the view
#         response = view.get(request)

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Assert that the response contains the 'subscriptions_list.html' template
#         self.assertTemplateUsed(
#             response, "multitenancy/subscriptions/subscriptions_list.html"
#         )

#     # Test that the SubscriptionsListView displays a list of all subscriptions
#     def test_display_all_subscriptions(self):
#         # Create some subscription objects
#         subscription1 = Subscription.objects.create()
#         subscription2 = Subscription.objects.create()

#         # Make a GET request to the SubscriptionsListView
#         response = self.client.get("/subscriptions/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the subscriptions are present in the response context
#         self.assertIn(subscription1, response.context["object_list"])
#         self.assertIn(subscription2, response.context["object_list"])

#         # Check that the subscriptions are displayed in the response content
#         self.assertContains(response, str(subscription1))
#         self.assertContains(response, str(subscription2))

#     # Test that a message is displayed if there are no subscriptions
#     def test_display_message_if_no_subscriptions(self):
#         # Create a test client
#         client = Client()

#         # Make a GET request to the subscriptions list view
#         response = client.get("/subscriptions/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the response contains the message for no subscriptions
#         self.assertContains(response, "No subscriptions found.")

#     # Test that the SubscriptionsListView class allows pagination of subscriptions
#     def test_pagination(self):
#         # Create some dummy subscription objects
#         subscriptions = []
#         for i in range(10):
#             subscription = Subscription.objects.create()
#             subscriptions.append(subscription)

#         # Set up the test client
#         client = Client()

#         # Log in as an admin user
#         user = User.objects.create_user(username="admin", password="admin")
#         client.login(username="admin", password="admin")

#         # Make a GET request to the subscriptions list view
#         response = client.get("/subscriptions/")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the subscriptions are paginated correctly
#         self.assertEqual(len(response.context["object_list"]), 5)
#         self.assertEqual(response.context["paginator"].num_pages, 2)
#         self.assertEqual(response.context["paginator"].count, 10)

#     # Test that the SubscriptionsListView class allows filtering of subscriptions by status
#     def test_filter_subscriptions_by_status(self):
#         # Create test data
#         active_subscription = Subscription.objects.create(status="active")
#         inactive_subscription = Subscription.objects.create(status="inactive")
#         cancelled_subscription = Subscription.objects.create(status="cancelled")
#         expired_subscription = Subscription.objects.create(status="expired")

#         # Make a GET request to the subscriptions list view with status filter
#         response = self.client.get("/subscriptions/?status=active")

#         # Check that only active subscriptions are returned in the response
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, active_subscription.pk)
#         self.assertNotContains(response, inactive_subscription.pk)
#         self.assertNotContains(response, cancelled_subscription.pk)
#         self.assertNotContains(response, expired_subscription.pk)

#     # Test that the SubscriptionsListView redirects to the login page when the user is not authenticated
#     def test_user_not_authenticated(self):
#         # Arrange
#         client = Client()

#         # Act
#         response = client.get("/subscriptions/")

#         # Assert
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, "/login/")

#     # Test that the SubscriptionsListView redirects to a permission denied page when the user is not an admin
#     def test_user_not_admin(self):
#         # Create a non-admin user
#         user = User.objects.create_user(username="testuser", password="testpassword")
#         # Log in the user
#         self.client.login(username="testuser", password="testpassword")

#         # Make a GET request to the SubscriptionsListView
#         response = self.client.get("/subscriptions/")

#         # Assert that the response status code is 403 (Forbidden)
#         self.assertEqual(response.status_code, 403)

#         # Assert that the response contains the permission denied message
#         self.assertContains(response, "Permission Denied")

#     # Test that the SubscriptionsListView handles the case when there are no subscriptions by displaying a message indicating that there are no subscriptions.
#     def test_no_subscriptions(self):
#         # Create a request object
#         request = HttpRequest()

#         # Create an instance of SubscriptionsListView
#         view = SubscriptionsListView()

#         # Set the request object on the view
#         view.request = request

#         # Call the get method on the view
#         response = view.get(request)

#         # Assert that the response contains the expected message
#         self.assertContains(response, "No subscriptions found")

#     # Test that the SubscriptionsListView class handles the case when there is only one subscription
#     def test_handles_one_subscription(self):
#         # Create a single subscription
#         subscription = Subscription.objects.create()

#         # Create a request object
#         request = HttpRequest()
#         request.user = User.objects.create()

#         # Create an instance of SubscriptionsListView
#         view = SubscriptionsListView()
#         view.request = request

#         # Set the model and template_name attributes
#         view.model = Subscription
#         view.template_name = "multitenancy/subscriptions/subscriptions_list.html"

#         # Call the get_queryset method
#         queryset = view.get_queryset()

#         # Assert that the queryset contains only the created subscription
#         self.assertEqual(list(queryset), [subscription])

#     # Test that the SubscriptionsListView class handles the case when there are many subscriptions
#     def test_many_subscriptions(self):
#         # Create multiple subscriptions
#         subscription1 = Subscription.objects.create(status="active")
#         subscription2 = Subscription.objects.create(status="active")
#         subscription3 = Subscription.objects.create(status="inactive")

#         # Set up the request and view
#         request = self.client.get("/subscriptions/")
#         view = SubscriptionsListView.as_view()

#         # Get the response
#         response = view(request)

#         # Check that the response contains the correct number of subscriptions
#         self.assertEqual(len(response.context_data["object_list"]), 2)

#         # Check that the response contains the correct subscriptions
#         self.assertIn(subscription1, response.context_data["object_list"])
#         self.assertIn(subscription2, response.context_data["object_list"])
#         self.assertNotIn(subscription3, response.context_data["object_list"])

#     # Test that the subscriptions in the SubscriptionsListView can be sorted by different fields
#     def test_sort_subscriptions_by_field(self):
#         # Create test data
#         subscription1 = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date(2022, 1, 1),
#             created_date=datetime.date(2022, 1, 1),
#             end_date=datetime.date(2022, 1, 31),
#             renewal_date=datetime.date(2022, 1, 31),
#             reference="Test Reference 1",
#             status="active",
#         )
#         subscription2 = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date(2022, 2, 1),
#             created_date=datetime.date(2022, 2, 1),
#             end_date=datetime.date(2022, 2, 28),
#             renewal_date=datetime.date(2022, 2, 28),
#             reference="Test Reference 2",
#             status="active",
#         )
#         subscription3 = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date(2022, 3, 1),
#             created_date=datetime.date(2022, 3, 1),
#             end_date=datetime.date(2022, 3, 31),
#             renewal_date=datetime.date(2022, 3, 31),
#             reference="Test Reference 3",
#             status="active",
#         )

#         # Make GET request to SubscriptionsListView with different sorting parameters
#         response1 = self.client.get("/subscriptions/?sort=created_date")
#         response2 = self.client.get("/subscriptions/?sort=start_date")
#         response3 = self.client.get("/subscriptions/?sort=end_date")

#         # Assert that the subscriptions are sorted correctly
#         self.assertEqual(
#             response1.context_data["object_list"],
#             [subscription3, subscription2, subscription1],
#         )
#         self.assertEqual(
#             response2.context_data["object_list"],
#             [subscription1, subscription2, subscription3],
#         )
#         self.assertEqual(
#             response3.context_data["object_list"],
#             [subscription1, subscription2, subscription3],
#         )

#     # Test that the SubscriptionsListView allows searching of subscriptions by reference
#     def test_search_by_reference(self):
#         # Create a test subscription
#         subscription = Subscription.objects.create(reference="Test Reference")

#         # Create a request object with a search parameter
#         request = self.client.get("/subscriptions/", {"search": "Test Reference"})

#         # Get the response
#         response = SubscriptionsListView.as_view()(request)

#         # Check that the subscription is in the response context
#         self.assertIn(subscription, response.context_data["object_list"])

#     # Test that the SubscriptionsListView displays the start date, end date, and renewal date of each subscription
#     def test_display_subscription_dates(self):
#         # Create a subscription object
#         subscription = Subscription.objects.create()

#         # Create a request object
#         request = HttpRequest()
#         request.user = User.objects.create(username="admin", type="Admin")

#         # Create a response object
#         response = SubscriptionsListView.as_view()(request)

#         # Check that the response contains the subscription dates
#         self.assertContains(response, subscription.start_date)
#         self.assertContains(response, subscription.end_date)
#         self.assertContains(response, subscription.renewal_date)

#     # Test that the SubscriptionsListView displays the product type of each subscription
#     def test_display_product_type(self):
#         # Create a subscription with a product type
#         product_type = ProductType.objects.create(name="Test Product Type")
#         subscription = Subscription.objects.create(product_type=product_type)

#         # Create a request and response objects
#         request = HttpRequest()
#         response = SubscriptionsListView.as_view()(request)

#         # Check that the response contains the product type of the subscription
#         self.assertContains(response, product_type.name)

#     # Test that the SubscriptionsListView displays the reason for the state change of each subscription
#     def test_display_reason_for_state_change(self):
#         # Create a subscription with a reason for state change
#         subscription = Subscription.objects.create(reason="Test Reason")

#         # Create a request object
#         request = HttpRequest()
#         request.user = User.objects.create(username="admin", type="Admin")

#         # Create an instance of SubscriptionsListView
#         view = SubscriptionsListView()
#         view.request = request

#         # Call the get method of SubscriptionsListView
#         response = view.get(request)

#         # Check that the response contains the reason for state change
#         self.assertContains(response, "Test Reason")


# class TestPlanViewSet(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the 'list' action of the PlanViewSet retrieves a list of plans
#     def test_retrieve_list_of_plans(self):
#         # Create some plans
#         plan1 = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Plan 1 description", price=100
#         )
#         plan2 = Plan.objects.create(
#             name="Plan 2", slug="plan-2", description="Plan 2 description", price=200
#         )

#         # Make a GET request to retrieve the list of plans
#         response = self.client.get("/plans/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the response data contains the correct number of plans
#         self.assertEqual(len(response.data), 2)

#         # Check that the response data contains the correct plan details
#         self.assertEqual(response.data[0]["name"], plan1.name)
#         self.assertEqual(response.data[0]["slug"], plan1.slug)
#         self.assertEqual(response.data[0]["description"], plan1.description)
#         self.assertEqual(response.data[0]["price"], str(plan1.price))

#         self.assertEqual(response.data[1]["name"], plan2.name)
#         self.assertEqual(response.data[1]["slug"], plan2.slug)
#         self.assertEqual(response.data[1]["description"], plan2.description)
#         self.assertEqual(response.data[1]["price"], str(plan2.price))

#     # Test that the retrieve action on PlanViewSet returns the specific plan requested
#     def test_retrieve_specific_plan(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Make a GET request to retrieve the plan
#         response = self.client.get(f"/plans/{plan.id}/")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the retrieved plan matches the created plan
#         self.assertEqual(response.data["id"], plan.id)
#         self.assertEqual(response.data["name"], plan.name)
#         self.assertEqual(response.data["slug"], plan.slug)
#         self.assertEqual(response.data["description"], plan.description)
#         self.assertEqual(response.data["price"], str(plan.price))
#         self.assertEqual(response.data["price_weekly"], str(plan.price_weekly))
#         self.assertEqual(response.data["price_quartely"], str(plan.price_quartely))
#         self.assertEqual(response.data["price_annually"], str(plan.price_annually))
#         self.assertEqual(len(response.data["features"]), plan.features.count())

#     # Test that a new plan can be created
#     def test_create_new_plan(self):
#         # Create a new plan
#         plan_data = {
#             "name": "Test Plan",
#             "description": "This is a test plan",
#             "price": 100,
#             "features": [],
#         }
#         response = self.client.post("/plans/", plan_data)

#         # Assert that the plan was created successfully
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Plan.objects.count(), 1)
#         self.assertEqual(Plan.objects.first().name, "Test Plan")

#     # Test that the update_existing_plan function updates an existing plan correctly
#     def test_update_existing_plan(self):
#         # Create a plan
#         plan = Plan.objects.create(
#             name="Basic", slug="basic", description="Basic plan", price=50
#         )

#         # Update the plan
#         updated_data = {"name": "Premium", "description": "Premium plan", "price": 100}
#         serializer = PlanSerialiser(instance=plan, data=updated_data, partial=True)
#         serializer.is_valid()
#         serializer.save()

#         # Retrieve the updated plan
#         updated_plan = Plan.objects.get(id=plan.id)

#         # Check that the plan has been updated correctly
#         self.assertEqual(updated_plan.name, "Premium")
#         self.assertEqual(updated_plan.description, "Premium plan")
#         self.assertEqual(updated_plan.price, 100)

#     # Test that an existing plan is successfully deleted
#     def test_delete_existing_plan(self):
#         # Create a new plan
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Delete the plan
#         response = self.client.delete(f"/plans/{plan.id}/")

#         # Check that the plan is deleted
#         self.assertEqual(response.status_code, 204)
#         self.assertFalse(Plan.objects.filter(id=plan.id).exists())

#     # Test that creating a plan with a name that already exists raises a validation error
#     def test_create_plan_with_existing_name(self):
#         # Create a plan with a name that already exists
#         existing_plan = Plan.objects.create(name="Basic Plan")
#         serializer = PlanSerialiser(data={"name": "Basic Plan"})
#         self.assertFalse(serializer.is_valid())
#         self.assertEqual(
#             serializer.errors["name"][0], "Plan with this name already exists."
#         )

#     # Test that a plan with an invalid price cannot be created
#     def test_create_plan_with_invalid_price(self):
#         # Create a plan with an invalid price
#         invalid_price = -50
#         plan_data = {
#             "name": "Basic Plan",
#             "description": "This is a basic plan",
#             "price": invalid_price,
#             "features": [],
#         }
#         serializer = PlanSerialiser(data=plan_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertEqual(
#             serializer.errors["price"][0],
#             "Ensure this value is greater than or equal to 0.",
#         )

#     # Test that updating a plan with a name that already exists raises an error
#     def test_update_plan_with_existing_name(self):
#         # Create a plan with a unique name
#         plan1 = Plan.objects.create(
#             name="Plan 1", slug="plan-1", description="Description 1", price=100
#         )

#         # Create another plan with a unique name
#         plan2 = Plan.objects.create(
#             name="Plan 2", slug="plan-2", description="Description 2", price=200
#         )

#         # Try to update plan2 with the same name as plan1
#         data = {
#             "name": "Plan 1",
#             "slug": "plan-1-updated",
#             "description": "Updated description",
#             "price": 150,
#         }
#         serializer = PlanSerialiser(plan2, data=data)
#         self.assertFalse(serializer.is_valid())
#         self.assertEqual(
#             serializer.errors["name"][0], "Plan with this Name already exists."
#         )

#     # Test that updating a plan with an invalid price raises an error
#     def test_update_plan_with_invalid_price(self):
#         # Create a plan
#         plan = Plan.objects.create(name="Basic", slug="basic", price=100)

#         # Update the plan with an invalid price
#         plan.price = -50
#         with self.assertRaises(ValidationError):
#             plan.save()

#     # Test that deleting a plan that does not exist returns a 404 status code
#     def test_delete_nonexistent_plan(self):
#         # Create a new plan
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Delete the plan
#         response = self.client.delete(f"/plans/{plan.id + 1}/")

#         # Assert that the response status code is 404
#         self.assertEqual(response.status_code, 404)

#     # Test that the serializer returns the correct values for the computed fields price_weekly, price_quartely, and price_annually
#     def test_computed_fields(self):
#         plan = Plan(name="Test Plan", price=100)
#         serializer = PlanSerialiser(plan)

#         expected_price_weekly = 100 / 4
#         expected_price_quartely = 100 * 3
#         expected_price_annually = 100 * 12

#         self.assertEqual(serializer.data["price_weekly"], expected_price_weekly)
#         self.assertEqual(serializer.data["price_quartely"], expected_price_quartely)
#         self.assertEqual(serializer.data["price_annually"], expected_price_annually)

#     # Test that the serializer returns all the expected fields
#     def test_serializer_fields(self):
#         # Create a plan object
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Create a product feature object
#         feature = ProductFeature.objects.create(name="Test Feature")

#         # Add the feature to the plan
#         plan.features.add(feature)

#         # Create a serializer instance
#         serializer = PlanSerialiser(plan)

#         # Check that the serializer returns all the expected fields
#         self.assertEqual(serializer.data["id"], plan.id)
#         self.assertEqual(serializer.data["name"], plan.name)
#         self.assertEqual(serializer.data["description"], plan.description)
#         self.assertEqual(serializer.data["price"], plan.price)
#         self.assertEqual(serializer.data["price_weekly"], plan.price_weekly)
#         self.assertEqual(serializer.data["price_quartely"], plan.price_quartely)
#         self.assertEqual(serializer.data["price_annually"], plan.price_annually)
#         self.assertEqual(serializer.data["slug"], plan.slug)
#         self.assertEqual(serializer.data["features"][0]["name"], feature.name)

#     # Test that the perform_create method sets the owner correctly
#     def test_perform_create_sets_owner_correctly(self):
#         # Create a user
#         user = User.objects.create(username="testuser")

#         # Create a plan
#         plan = Plan.objects.create(name="Test Plan", slug="test-plan", price=100)

#         # Create a request with the user as the authenticated user
#         request = RequestFactory().post(
#             "/plans/", {"name": "Test Plan", "slug": "test-plan", "price": 100}
#         )
#         force_authenticate(request, user=user)

#         # Create a serializer with the request
#         serializer = PlanSerialiser(data=request.data, context={"request": request})
#         serializer.is_valid()

#         # Call the perform_create method
#         view = PlanViewSet()
#         view.perform_create(serializer)

#         # Check that the owner of the plan is set correctly
#         self.assertEqual(serializer.validated_data["owner"], user)

#     # Test that the queryset of PlanViewSet only returns plans owned by the current user
#     def test_queryset_returns_owned_plans(self):
#         # Create a user
#         user = User.objects.create(username="testuser")

#         # Create plans owned by the user
#         plan1 = Plan.objects.create(name="Plan 1", owner=user)
#         plan2 = Plan.objects.create(name="Plan 2", owner=user)

#         # Create a plan not owned by the user
#         plan3 = Plan.objects.create(name="Plan 3")

#         # Set the request user to the created user
#         self.request.user = user

#         # Call the perform_create method of PlanViewSet
#         queryset = PlanViewSet.queryset

#         # Assert that the queryset only contains plans owned by the current user
#         self.assertEqual(queryset.count(), 2)
#         self.assertIn(plan1, queryset)
#         self.assertIn(plan2, queryset)
#         self.assertNotIn(plan3, queryset)

#     # Test that the serializer returns the expected values for the features field in the PlanViewSet class
#     def test_serializer_returns_expected_values_for_features_field(self):
#         # Create a Plan object
#         plan = Plan.objects.create(
#             name="Test Plan",
#             slug="test-plan",
#             description="Test Description",
#             price=100,
#         )

#         # Create two ProductFeature objects
#         feature1 = ProductFeature.objects.create(name="Feature 1")
#         feature2 = ProductFeature.objects.create(name="Feature 2")

#         # Add the features to the plan
#         plan.features.add(feature1, feature2)

#         # Create a serializer instance
#         serializer = PlanSerialiser(plan)

#         # Check that the features field in the serializer contains the expected values
#         expected_features = [
#             {"id": feature1.id, "name": "Feature 1"},
#             {"id": feature2.id, "name": "Feature 2"},
#         ]
#         self.assertEqual(serializer.data["features"], expected_features)


# class TestProductTypeListView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the view returns HTTP status code 200 when accessed by an authenticated admin user.
#     def test_view_returns_200_for_authenticated_admin_user(self):
#         # Create an authenticated admin user
#         admin_user = User.objects.create(username="admin", type="Admin")
#         self.client.force_login(admin_user)

#         # Access the view
#         response = self.client.get("/product-type-list/")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#     # Test that the view returns a list of all ProductType objects when accessed by an authenticated admin user.
#     def test_view_returns_all_product_types_for_authenticated_admin_user(self):
#         # Create an authenticated admin user
#         admin_user = User.objects.create(username="admin", type="Admin")
#         self.client.force_login(admin_user)

#         # Access the view
#         response = self.client.get("/product-types/")

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the returned object list contains all ProductType objects
#         product_types = ProductType.objects.all()
#         self.assertQuerysetEqual(
#             response.context["object_list"], product_types, transform=lambda x: x
#         )


# class TestSubscriptionsViewSet(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the 'list' action of the SubscriptionsViewSet retrieves a list of all subscriptions
#     def test_retrieve_all_subscriptions(self):
#         # Create some sample subscriptions
#         subscription1 = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today(),
#             created_date=datetime.date.today(),
#             renewal_date=datetime.date.today(),
#             reference="Reference 1",
#             last_updated=datetime.datetime.now(),
#             product_type=ProductType.objects.create(name="Product Type 1"),
#             reason="Reason 1",
#             status="active",
#         )
#         subscription2 = Subscription.objects.create(
#             cycle="weekly",
#             subscription_duration=7,
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today(),
#             created_date=datetime.date.today(),
#             renewal_date=datetime.date.today(),
#             reference="Reference 2",
#             last_updated=datetime.datetime.now(),
#             product_type=ProductType.objects.create(name="Product Type 2"),
#             reason="Reason 2",
#             status="inactive",
#         )

#         # Make a GET request to retrieve all subscriptions
#         response = self.client.get("/subscriptions/")

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Assert that the response data contains the correct number of subscriptions
#         self.assertEqual(len(response.data), 2)

#         # Assert that the response data contains the correct subscription details
#         self.assertEqual(response.data[0]["cycle"], subscription1.cycle)
#         self.assertEqual(
#             response.data[0]["subscription_duration"],
#             subscription1.subscription_duration,
#         )
#         self.assertEqual(
#             response.data[0]["start_date"],
#             subscription1.start_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(
#             response.data[0]["end_date"], subscription1.end_date.strftime("%Y-%m-%d")
#         )
#         self.assertEqual(
#             response.data[0]["created_date"],
#             subscription1.created_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(
#             response.data[0]["renewal_date"],
#             subscription1.renewal_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(response.data[0]["reference"], subscription1.reference)
#         self.assertEqual(
#             response.data[0]["last_updated"],
#             subscription1.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#         )
#         self.assertEqual(
#             response.data[0]["product_type"]["name"], subscription1.product_type.name
#         )
#         self.assertEqual(response.data[0]["reason"], subscription1.reason)
#         self.assertEqual(response.data[0]["status"], subscription1.status)

#         self.assertEqual(response.data[1]["cycle"], subscription2.cycle)
#         self.assertEqual(
#             response.data[1]["subscription_duration"],
#             subscription2.subscription_duration,
#         )
#         self.assertEqual(
#             response.data[1]["start_date"],
#             subscription2.start_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(
#             response.data[1]["end_date"], subscription2.end_date.strftime("%Y-%m-%d")
#         )
#         self.assertEqual(
#             response.data[1]["created_date"],
#             subscription2.created_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(
#             response.data[1]["renewal_date"],
#             subscription2.renewal_date.strftime("%Y-%m-%d"),
#         )
#         self.assertEqual(response.data[1]["reference"], subscription2.reference)
#         self.assertEqual(
#             response.data[1]["last_updated"],
#             subscription2.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#         )
#         self.assertEqual(
#             response.data[1]["product_type"]["name"], subscription2.product_type.name
#         )
#         self.assertEqual(response.data[1]["reason"], subscription2.reason)
#         self.assertEqual(response.data[1]["status"], subscription2.status)

#     # Test that the 'retrieve' action of the SubscriptionsViewSet retrieves the correct subscription when given a valid ID
#     def test_retrieve_subscription_by_id(self):
#         # Create a subscription
#         subscription = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today(),
#             created_date=datetime.date.today(),
#             renewal_date=datetime.date.today(),
#             reference="Test Subscription",
#             last_updated=datetime.datetime.now(),
#             product_type=None,
#             reason="Test Reason",
#             status="active",
#         )

#         # Retrieve the subscription by ID
#         response = self.client.get(f"/subscriptions/{subscription.id}/")

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the retrieved subscription data matches the created subscription
#         self.assertEqual(response.data["id"], subscription.id)
#         self.assertEqual(response.data["cycle"], subscription.cycle)
#         self.assertEqual(
#             response.data["subscription_duration"], subscription.subscription_duration
#         )
#         self.assertEqual(
#             response.data["start_date"], subscription.start_date.isoformat()
#         )
#         self.assertEqual(response.data["end_date"], subscription.end_date.isoformat())
#         self.assertEqual(
#             response.data["created_date"], subscription.created_date.isoformat()
#         )
#         self.assertEqual(
#             response.data["renewal_date"], subscription.renewal_date.isoformat()
#         )
#         self.assertEqual(response.data["reference"], subscription.reference)
#         self.assertEqual(
#             response.data["last_updated"], subscription.last_updated.isoformat()
#         )
#         self.assertEqual(response.data["product_type"], None)
#         self.assertEqual(response.data["reason"], subscription.reason)
#         self.assertEqual(response.data["status"], subscription.status)

#     # Test that a new subscription is created successfully
#     def test_create_new_subscription(self):
#         # Create a new subscription
#         subscription_data = {
#             "cycle": "monthly",
#             "subscription_duration": 30,
#             "start_date": "2022-01-01",
#             "end_date": "2022-01-31",
#             "created_date": "2022-01-01",
#             "renewal_date": "2022-01-01",
#             "reference": "Test Subscription",
#             "last_updated": "2022-01-01",
#             "product_type": {"id": 1, "name": "Product Type 1"},
#             "reason": "New Subscription",
#             "status": "active",
#         }
#         response = self.client.post("/subscriptions/", subscription_data, format="json")

#         # Assert that the response status code is 201 (Created)
#         self.assertEqual(response.status_code, 201)

#         # Assert that the subscription is created in the database
#         self.assertEqual(Subscription.objects.count(), 1)

#         # Assert that the created subscription has the correct data
#         subscription = Subscription.objects.first()
#         self.assertEqual(subscription.cycle, "monthly")
#         self.assertEqual(subscription.subscription_duration, 30)
#         self.assertEqual(subscription.start_date, datetime.date(2022, 1, 1))
#         self.assertEqual(subscription.end_date, datetime.date(2022, 1, 31))
#         self.assertEqual(subscription.created_date, datetime.date(2022, 1, 1))
#         self.assertEqual(subscription.renewal_date, datetime.date(2022, 1, 1))
#         self.assertEqual(subscription.reference, "Test Subscription")
#         self.assertEqual(subscription.last_updated, datetime.date(2022, 1, 1))
#         self.assertEqual(subscription.product_type.id, 1)
#         self.assertEqual(subscription.product_type.name, "Product Type 1")
#         self.assertEqual(subscription.reason, "New Subscription")
#         self.assertEqual(subscription.status, "active")

#     # Test that the update_existing_subscription function updates an existing subscription correctly
#     def test_update_existing_subscription(self):
#         # Create a subscription object
#         subscription = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today() + datetime.timedelta(days=30),
#             created_date=datetime.date.today(),
#             renewal_date=datetime.date.today(),
#             reference="Test Subscription",
#             last_updated=datetime.datetime.now(),
#             product_type=ProductType.objects.create(name="Test Product Type"),
#             reason="Test Reason",
#             status="active",
#         )

#         # Update the subscription
#         updated_data = {
#             "cycle": "weekly",
#             "subscription_duration": 7,
#             "start_date": datetime.date.today(),
#             "end_date": datetime.date.today() + datetime.timedelta(days=7),
#             "created_date": datetime.date.today(),
#             "renewal_date": datetime.date.today(),
#             "reference": "Updated Subscription",
#             "last_updated": datetime.datetime.now(),
#             "product_type": {"name": "Updated Product Type"},
#             "reason": "Updated Reason",
#             "status": "inactive",
#         }
#         serializer = SubscriptionSerializer(subscription, data=updated_data)
#         if serializer.is_valid():
#             serializer.save()

#         # Retrieve the updated subscription
#         updated_subscription = Subscription.objects.get(pk=subscription.pk)

#         # Assert that the subscription has been updated correctly
#         self.assertEqual(updated_subscription.cycle, "weekly")
#         self.assertEqual(updated_subscription.subscription_duration, 7)
#         self.assertEqual(updated_subscription.start_date, datetime.date.today())
#         self.assertEqual(
#             updated_subscription.end_date,
#             datetime.date.today() + datetime.timedelta(days=7),
#         )
#         self.assertEqual(updated_subscription.created_date, datetime.date.today())
#         self.assertEqual(updated_subscription.renewal_date, datetime.date.today())
#         self.assertEqual(updated_subscription.reference, "Updated Subscription")
#         self.assertEqual(updated_subscription.last_updated, datetime.datetime.now())
#         self.assertEqual(updated_subscription.product_type.name, "Updated Product Type")
#         self.assertEqual(updated_subscription.reason, "Updated Reason")
#         self.assertEqual(updated_subscription.status, "inactive")

#     # Test that an existing subscription is deleted successfully
#     def test_delete_subscription(self):
#         # Create a subscription object
#         subscription = Subscription.objects.create(
#             cycle="monthly",
#             subscription_duration=30,
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today(),
#             created_date=datetime.date.today(),
#             renewal_date=datetime.date.today(),
#             reference="Test Reference",
#             last_updated=datetime.datetime.now(),
#             product_type=None,
#             reason="Test Reason",
#             status="active",
#         )

#         # Get the subscription ID
#         subscription_id = subscription.id

#         # Delete the subscription
#         response = self.client.delete(f"/subscriptions/{subscription_id}/")

#         # Check that the response status code is 204 (No Content)
#         self.assertEqual(response.status_code, 204)

#         # Check that the subscription is no longer in the database
#         with self.assertRaises(Subscription.DoesNotExist):
#             Subscription.objects.get(id=subscription_id)


# class TestProductTypeViewSet(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that the viewset returns a list of all ProductTypes.
#     def test_list_all_product_types(self):
#         # Create some ProductTypes
#         product_type1 = ProductType.objects.create(name="Tenant App")
#         product_type2 = ProductType.objects.create(name="Custom Domain")
#         product_type3 = ProductType.objects.create(name="3rd party App")

#         # Make a GET request to the viewset
#         response = self.client.get("/product-types/")

#         # Check that the response status code is 200 OK
#         self.assertEqual(response.status_code, 200)

#         # Check that the response data contains all the ProductTypes
#         self.assertEqual(len(response.data), 3)
#         self.assertEqual(response.data[0]["name"], product_type1.name)
#         self.assertEqual(response.data[1]["name"], product_type2.name)
#         self.assertEqual(response.data[2]["name"], product_type3.name)

#     # Test that the viewset can create a new ProductType by calling the perform_create method with a serializer.
#     def test_create_new_product_type(self):
#         # Create a user for the request
#         user = User.objects.create(username="testuser")

#         # Create a request object with the user
#         request = RequestFactory().post("/product_types/", {"name": "New Product Type"})
#         force_authenticate(request, user=user)

#         # Create a serializer with the request data
#         serializer = ProductTypeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Create an instance of the viewset
#         viewset = ProductTypeViewSet()

#         # Call the perform_create method with the serializer
#         viewset.perform_create(serializer)

#         # Assert that a new ProductType has been created
#         self.assertEqual(ProductType.objects.count(), 1)
#         new_product_type = ProductType.objects.first()
#         self.assertEqual(new_product_type.name, "New Product Type")
#         self.assertEqual(new_product_type.owner, user)

#     # Test that the viewset can successfully retrieve a single ProductType by its id.
#     def test_retrieve_product_type_by_id(self):
#         # Create a ProductType instance
#         product_type = ProductType.objects.create(name="Test Product Type")

#         # Make a GET request to retrieve the ProductType by its id
#         response = self.client.get(f"/product-types/{product_type.id}/")

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Assert that the retrieved ProductType matches the created ProductType
#         self.assertEqual(response.data["id"], product_type.id)
#         self.assertEqual(response.data["name"], product_type.name)

#     # Test that the viewset can successfully update an existing ProductType.
#     def test_update_existing_product_type(self):
#         # Create a ProductType object
#         product_type = ProductType.objects.create(name="Test Product Type")

#         # Update the ProductType object
#         updated_name = "Updated Product Type"
#         data = {"name": updated_name}
#         response = self.client.put(f"/product-types/{product_type.id}/", data=data)

#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)

#         # Check that the ProductType object has been updated
#         product_type.refresh_from_db()
#         self.assertEqual(product_type.name, updated_name)

#     # Test that the viewset can successfully delete an existing ProductType.
#     def test_delete_product_type(self):
#         # Create a ProductType instance
#         product_type = ProductType.objects.create(name="Test Product Type")

#         # Make a DELETE request to delete the ProductType
#         response = self.client.delete(f"/product-types/{product_type.id}/")

#         # Check that the response status code is 204 (No Content)
#         self.assertEqual(response.status_code, 204)

#         # Check that the ProductType instance has been deleted from the database
#         self.assertFalse(ProductType.objects.filter(id=product_type.id).exists())


# class TestPlanView(unittest.TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     # Test that a new tenant is created with a valid plan and subscription duration
#     def test_create_new_tenant_with_valid_plan_and_subscription_duration(self):
#         # Create a mock request with the necessary data
#         request = Mock()
#         request.body = json.dumps({"subscription_duration": 30, "plan": 1})
#         request.user = Mock()
#         request.user.is_active = True

#         # Create a mock Plan object
#         plan = Mock()
#         plan.name = "Basic Plan"
#         plan.id = 1

#         # Create a mock User object
#         user = Mock()
#         user.username = "testuser"

#         # Create a mock Subscription object
#         subscription = Mock()

#         # Create a mock Tenant object
#         tenant = Mock()

#         # Create a mock DomainModel object
#         domain_model = Mock()

#         # Patch the necessary methods and attributes
#         with patch(
#             "json.loads", return_value={"subscription_duration": 30, "plan": 1}
#         ), patch("Plan.objects.get", return_value=plan), patch(
#             "request.user", return_value=user
#         ), patch(
#             "uuid.uuid1", return_value="mock_uuid"
#         ), patch(
#             "get_tenant_domain_model", return_value=domain_model
#         ), patch(
#             "DomainModel.objects.filter",
#             return_value=Mock(exists=Mock(return_value=False)),
#         ), patch(
#             "Subscription.objects.create", return_value=subscription
#         ), patch(
#             "Tenant.objects.create", return_value=tenant
#         ), patch(
#             "get_tenant_domain_model().objects.create", return_value=Mock()
#         ), patch(
#             "Tenant.add_user"
#         ), patch(
#             "sweetify.success"
#         ), patch(
#             "JsonResponse"
#         ) as mock_json_response:

#             # Create an instance of PlanView
#             plan_view = PlanView()

#             # Call the post method of PlanView
#             plan_view.post(request)

#         # Assert that the necessary methods and attributes were called
#         json_response_mock.assert_called_with({"plan": 1, "subscription_duration": 30})
#         subscription.start_subscription.assert_called_with("monthly")
#         tenant.add_user.assert_called_with(user, is_superuser=True, is_staff=True)
#         sweetify.success.assert_called_with(
#             request, "Successfully Created Tenant!", icon="success", timer=5000
#         )

#     # Test that the post method of PlanView returns a JSON response with the selected plan and duration
#     def test_return_json_response(self):
#         # Create a mock request object
#         request = MagicMock()
#         request.body = json.dumps({"plan": 1, "subscription_duration": 30})
#         request.user = MagicMock()
#         request.user.is_active = True

#         # Create a mock Plan object
#         plan = MagicMock()
#         plan.name = "Test Plan"
#         plan.id = 1

#         # Create a mock Subscription object
#         subscription = MagicMock()
#         subscription.start_subscription.return_value = 30

#         # Create a mock Tenant object
#         tenant = MagicMock()
#         tenant.add_user.return_value = None

#         # Create a mock DomainModel object
#         domain_model = MagicMock()
#         domain_model.objects.filter.return_value.exists.return_value = False

#         # Create a mock JsonResponse object
#         json_response = MagicMock()

#         # Patch the necessary objects and methods
#         with patch(
#             "json.loads", return_value={"plan": 1, "subscription_duration": 30}
#         ), patch("PlanView.Plan.objects.get", return_value=plan), patch(
#             "PlanView.Subscription.objects.create", return_value=subscription
#         ), patch(
#             "PlanView.Tenant.objects.create", return_value=tenant
#         ), patch(
#             "PlanView.get_tenant_domain_model", return_value=domain_model
#         ), patch(
#             "PlanView.JsonResponse", return_value=json_response
#         ) as mock_json_response:

#             # Create an instance of PlanView
#             plan_view = PlanView()

#             # Call the post method
#             result = plan_view.post(request)

#             # Assert that the JsonResponse was called with the correct arguments
#             mock_json_response.assert_called_with(
#                 {"plan": 1, "subscription_duration": 30}
#             )

#             # Assert that the result is equal to the JsonResponse object
#             self.assertEqual(result, json_response)
