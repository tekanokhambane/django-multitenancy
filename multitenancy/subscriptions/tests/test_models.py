# Generated by CodiumAI

import datetime
import unittest
from django.utils import timezone

from django.forms import ValidationError

from multitenancy.subscriptions.models import (
    Plan,
    ProductFeature,
    ProductType,
    Subscription,
)


class TestProductFeature(unittest.TestCase):

    # Test that a new instance of ProductFeature can be created with valid name and description
    def test_create_new_instance(self):
        name = "Feature 1"
        description = "This is a feature"
        feature = ProductFeature(name=name, description=description)
        self.assertEqual(feature.name, name)
        self.assertEqual(feature.description, description)

    # Test that the name of a ProductFeature instance can be retrieved correctly.
    def test_get_name(self):
        name = "Feature 1"
        description = "This is a feature"
        feature = ProductFeature(name=name, description=description)
        self.assertEqual(feature.name, name)

    # Test that a new instance of ProductFeature cannot be created with an empty name.
    def test_empty_name(self):
        feature = ProductFeature(name="")
        with self.assertRaises(ValueError):
            feature.save()

    # Test that multiple instances of ProductFeature are ordered by primary key in descending order.
    def test_order_by_primary_key(self):
        feature1 = ProductFeature.objects.create(
            name="Feature 1", description="This is feature 1"
        )
        feature2 = ProductFeature.objects.create(
            name="Feature 2", description="This is feature 2"
        )
        feature3 = ProductFeature.objects.create(
            name="Feature 3", description="This is feature 3"
        )

        features = ProductFeature.objects.all()
        self.assertEqual(features[0], feature3)
        self.assertEqual(features[1], feature2)
        self.assertEqual(features[2], feature1)


class TestPlan(unittest.TestCase):
    # Test that a Plan object can be created with all required fields and saved successfully
    def test_create_plan_and_save_successfully(self):
        plan, created = Plan.objects.get_or_create(
            name="basic", slug="basic", description="Basic plan", price=75
        )
        self.assertEqual(plan.name, "basic")
        self.assertEqual(plan.slug, "basic")
        self.assertEqual(plan.description, "Basic plan")
        self.assertEqual(plan.price, 75)
        self.assertTrue(plan.pk is not None)

    # Test that a feature can be added to a Plan object and saved successfully
    def test_add_feature_and_save_successfully(self):
        plan, created = Plan.objects.get_or_create(name="free")
        plan.add_feature("Free domain")
        features = plan.features.all()
        for feature in features:
            self.assertEquals(feature.name, "Free domain")
        self.assertEquals(plan.name, "free")

    # Test that a Plan object can be retrieved by name or description using the search method
    def test_retrieve_plan_by_search(self):
        # Create a Plan object
        plan = Plan.objects.create(name="standard", description="Standard plan")

        # Search for the Plan object by name
        result_name = Plan.objects.search("standard")
        self.assertEqual(result_name.first(), plan)

        # Search for the Plan object by description
        result_description = Plan.objects.search("Standard plan")
        self.assertEqual(result_description.first(), plan)

    # Test that the active_plans method returns all active Plan objects
    def test_retrieve_active_plans(self):
        # Create active and inactive Plan objects
        active_plan1 = Plan.objects.create(name="Enterprise", is_active=True)
        active_plan2 = Plan.objects.create(name="Premium", is_active=True)
        inactive_plan = Plan.objects.create(name="Inactive", is_active=False)

        # Retrieve all active Plan objects
        active_plans = Plan.objects.active_plans()

        # Check that only the active Plan objects are returned
        self.assertIn(active_plan1, active_plans)
        self.assertIn(active_plan2, active_plans)
        self.assertNotIn(inactive_plan, active_plans)

    # Test that the by_price method of the Plan class retrieves all Plan objects with a specific price
    def test_retrieve_plans_by_price(self):
        # Create three Plan objects with different prices
        plan1 = Plan.objects.create(name="plus", price=50)
        plan2 = Plan.objects.create(name="standardplus", price=75)
        plan3 = Plan.objects.create(name="premium", price=100)

        # Retrieve all Plan objects with a price of 75
        plans = Plan.objects.by_price(75)

        # Check that only plan2 is retrieved
        self.assertEqual(len(plans), 10)
        self.assertEqual(plans[:-2], plan2)

    # Test that the by_features method of the Plan class retrieves all Plan objects with a specific feature
    def test_retrieve_plan_by_feature(self):
        # Create a ProductFeature object
        feature = ProductFeature.objects.create(
            name="Feature 1", description="Description 1"
        )

        # Create two Plan objects with the same feature
        plan1 = Plan.objects.create(name="Plan 1")
        plan1.features.add(feature)
        plan2 = Plan.objects.create(name="Plan 2")
        plan2.features.add(feature)

        # Create a Plan object without the feature
        plan3 = Plan.objects.create(name="Plan 3")

        # Retrieve all Plan objects with the feature using the by_features method
        plans = Plan.objects.by_features(feature)

        # Check that the retrieved plans include plan1 and plan2, but not plan3
        self.assertIn(plan1, plans)
        self.assertIn(plan2, plans)
        self.assertNotIn(plan3, plans)


#     # Test that creating a Plan object with a name that already exists raises a validation error
#     def test_duplicate_name_validation(self):
#         # Create a Plan object with a name that already exists
#         with self.assertRaises(ValidationError):
#             plan = Plan.objects.create(name="basic")
#             plan.save()

#     # Test that creating a Plan object without a name raises a validation error
#     def test_create_plan_without_name(self):
#         with self.assertRaises(ValidationError):
#             plan = Plan.objects.create()

#     # Test that creating a Plan object with a non-decimal price raises a validation error
#     def test_invalid_price(self):
#         with self.assertRaises(ValidationError):
#             plan = Plan(name="basic", price=100)

#     # Test that adding a feature to a Plan object that already exists raises a validation error
#     def test_add_existing_feature(self):
#         plan = Plan.objects.create(name="basic")
#         plan.add_feature("Free domain")
#         with self.assertRaises(ValidationError):
#             plan.add_feature("Free domain")

#     # Test that retrieving a Plan object that does not exist raises a DoesNotExist error
#     def test_retrieve_nonexistent_plan(self):
#         with self.assertRaises(Plan.DoesNotExist):
#             Plan.objects.get(name="nonexistent")

#     # Test that the slug field is automatically generated when a Plan object is saved without a slug
#     def test_slug_auto_generation(self):
#         plan = Plan(name="basic")
#         plan.save()
#         self.assertIsNotNone(plan.slug)

#     # Test that the price_weekly property of the Plan class returns the correct value
#     def test_price_weekly(self):
#         plan = Plan.objects.create(name="basic", price=100)
#         self.assertEqual(plan.price_weekly, 25)

#     # Test that the price_quartely property of the Plan class returns the correct value
#     def test_price_quartely(self):
#         plan = Plan.objects.create(name="basic", price=100)
#         self.assertEqual(plan.price_quartely, 300)

#     # Test that the price_annually property of the Plan class returns the correct value
#     def test_price_annually(self):
#         plan = Plan.objects.create(name="basic", price=100)
#         self.assertEqual(plan.price_annually, 1200)

#     # Test that the add_feature method can successfully add multiple features to a Plan object
#     def test_add_multiple_features(self):
#         plan = Plan.objects.get_or_create(name="basic")
#         plan.add_feature("Free domain")
#         plan.add_feature("SSL certificate")
#         features = plan.features.all()
#         self.assertEqual(len(features), 2)
#         self.assertEqual(features[0].name, "Free domain")
#         self.assertEqual(features[1].name, "SSL certificate")
#         self.assertEqual(plan.name, "basic")


# class TestProductType(unittest.TestCase):
#     # Test that a ProductType object is created with the default values
#     def test_create_product_type_with_default_values(self):
#         product_type = ProductType.objects.create()
#         self.assertEqual(product_type.name, ProductType.Types.TENANT_APP)

#     # Test that a ProductType object can be created with custom values
#     def test_create_product_type_with_custom_values(self):
#         # Create a ProductType object with custom values
#         product_type = ProductType.objects.create(name=ProductType.Types.DOMAIN)

#         # Assert that the object is created successfully
#         self.assertEqual(product_type.name, ProductType.Types.DOMAIN)

#     # Test that a ProductType object can be retrieved
#     def test_retrieve_product_type(self):
#         product_type = ProductType.objects.create(name=ProductType.Types.TENANT_APP)
#         retrieved_product_type = ProductType.objects.get(
#             name=ProductType.Types.TENANT_APP
#         )
#         self.assertEqual(product_type, retrieved_product_type)

#     # Test that the ProductType object is updated correctly
#     def test_update_product_type(self):
#         # Create a ProductType object
#         product_type = ProductType.objects.create(name=ProductType.Types.TENANT_APP)

#         # Update the ProductType object
#         product_type.name = ProductType.Types.DOMAIN
#         product_type.save()

#         # Check if the ProductType object is updated correctly
#         updated_product_type = ProductType.objects.get(pk=product_type.pk)
#         self.assertEqual(updated_product_type.name, ProductType.Types.DOMAIN)

#     # Test that a ProductType object is successfully deleted
#     def test_delete_product_type(self):
#         # Create a ProductType object
#         product_type = ProductType.objects.create(name=ProductType.Types.TENANT_APP)

#         # Delete the ProductType object
#         product_type.delete()

#         # Check that the ProductType object is deleted
#         self.assertFalse(ProductType.objects.filter(pk=product_type.pk).exists())

#     # Test that a ProductType object can be created with the maximum length of the name field
#     def test_create_product_type_with_max_length_name(self):
#         # Create a ProductType object with the maximum length of the name field
#         name = "a" * 115
#         product_type = ProductType.objects.create(name=name)

#         # Assert that the ProductType object is created successfully
#         self.assertEqual(product_type.name, name)

#     # Test that creating a ProductType object with an invalid name field raises a validation error
#     def test_invalid_name_field(self):
#         with self.assertRaises(ValidationError):
#             ProductType.objects.create(name="invalid_name")

#     # Test that a ProductType object cannot be created with a null name field
#     def test_create_product_type_with_null_name(self):
#         with self.assertRaises(ValueError):
#             ProductType.objects.create(name=None)

#     # Test that creating a ProductType object with a name field that already exists raises an error
#     def test_create_existing_name(self):
#         with self.assertRaises(Exception):
#             ProductType.objects.create(name=ProductType.Types.TENANT_APP)

#     # Test that the 'create_defaults' method of the ProductTypeManager class creates the default product types correctly
#     def test_create_defaults(self):
#         manager = ProductType.objects
#         manager.create_defaults()
#         # Assert that the default product types are created
#         self.assertEqual(
#             ProductType.objects.filter(name=ProductType.Types.TENANT_APP).count(), 1
#         )
#         self.assertEqual(
#             ProductType.objects.filter(name=ProductType.Types.DOMAIN).count(), 1
#         )
#         self.assertEqual(
#             ProductType.objects.filter(name=ProductType.Types.THIRD_PARTY_APP).count(),
#             1,
#         )

#     # Test that the 'subscriptions' related name attribute of the ForeignKey field is set correctly
#     def test_related_name_attribute(self):
#         product_type = ProductType.objects.create(name=ProductType.Types.TENANT_APP)
#         subscription = Subscription.objects.create(product_type=product_type)
#         self.assertEqual(subscription.product_type, product_type)
#         self.assertEqual(product_type.subscriptions.first(), subscription)

#     # Test that the 'Types' inner class of the ProductType class is defined correctly
#     def test_types_inner_class(self):
#         self.assertEqual(ProductType.Types.TENANT_APP, "tenant")
#         self.assertEqual(ProductType.Types.DOMAIN, "domain")
#         self.assertEqual(ProductType.Types.THIRD_PARTY_APP, "third_party")


# class TestSubscription(unittest.TestCase):
#     # Test that the 'start_subscription' method correctly starts a subscription with a weekly cycle
#     def test_start_subscription_weekly_cycle(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("weekly")

#         self.assertEquals(subscribe.status, "active")
#         self.assertEquals(subscribe.cycle, "weekly")
#         self.assertEquals(subscribe.reason, "Start Subscription")
#         self.assertEquals(subscribe.renewal_date, datetime.date.today())
#         self.assertEquals(
#             subscribe.end_date, datetime.date.today() + datetime.timedelta(days=7)
#         )
#         self.assertEquals(subscribe.subscription_duration, 7)

#     # Test that starting a subscription with a monthly cycle sets the correct attributes and dates
#     def test_start_subscription_monthly_cycle(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("monthly")

#         self.assertEquals(subscribe.status, "active")
#         self.assertEquals(subscribe.cycle, "monthly")
#         self.assertEquals(subscribe.reason, "Start Subscription")
#         self.assertEquals(subscribe.renewal_date, datetime.date.today())
#         self.assertEquals(
#             subscribe.end_date, datetime.date.today() + datetime.timedelta(days=30)
#         )
#         self.assertEquals(subscribe.subscription_duration, 30)

#     # Test that the start_subscription method sets the subscription status to active, cycle to quarterly, reason to "Start Subscription", renewal date to today, end date to today + 90 days, and subscription duration to 90.
#     def test_start_subscription_quarterly_cycle(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("quartely")

#         self.assertEquals(subscribe.status, "active")
#         self.assertEquals(subscribe.cycle, "quartely")
#         self.assertEquals(subscribe.reason, "Start Subscription")
#         self.assertEquals(subscribe.renewal_date, datetime.date.today())
#         self.assertEquals(
#             subscribe.end_date, datetime.date.today() + datetime.timedelta(days=90)
#         )
#         self.assertEquals(subscribe.subscription_duration, 90)

#     # Test that starting a subscription with an annual cycle sets the correct attributes and dates
#     def test_start_subscription_annual_cycle(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("annually")

#         self.assertEquals(subscribe.status, "active")
#         self.assertEquals(subscribe.cycle, "annually")
#         self.assertEquals(subscribe.reason, "Start Subscription")
#         self.assertEquals(subscribe.renewal_date, datetime.date.today())
#         self.assertEquals(
#             subscribe.end_date, datetime.date.today() + datetime.timedelta(days=365)
#         )
#         self.assertEquals(subscribe.subscription_duration, 365)

#     # Test that an active subscription can be successfully renewed
#     def test_renew_active_subscription(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("weekly")
#         subscribe.renew()

#         self.assertEquals(subscribe.reason, "Subscription renewed")

#     # Test that cancelling an active subscription sets the status to 'cancelled' and the end date to today's date.
#     def test_cancel_active_subscription(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("weekly")
#         subscribe.cancel_subscription()

#         self.assertEquals(subscribe.status, "cancelled")
#         self.assertEquals(subscribe.end_date, datetime.date.today())

#     # Test that an inactive subscription can be activated successfully
#     def test_activate_inactive_subscription(self):
#         # Create an inactive subscription
#         subscription = Subscription.objects.create(status="inactive")

#         # Activate the subscription
#         subscription.activate_subscription(30)

#         # Check if the subscription is now active
#         self.assertEqual(subscription.status, "active")

#         # Check if the renewal date is set to today
#         self.assertEqual(subscription.renewal_date, datetime.date.today())

#         # Check if the end date is set correctly based on the duration
#         self.assertEqual(
#             subscription.end_date, datetime.date.today() + datetime.timedelta(days=30)
#         )

#         # Check if the reason is updated correctly
#         self.assertEqual(subscription.reason, "Subscription activated")

#     # Test that the duration of a subscription is updated correctly
#     def test_update_duration(self):
#         subscribe = Subscription.objects.create()
#         subscribe.start_subscription("weekly")
#         subscribe.update_duration(14)

#         self.assertEquals(subscribe.subscription_duration, 14)

#     # Test that the is_active property of a Subscription instance returns True if the status is "active", and False otherwise.
#     def test_is_active_subscription(self):
#         # Create a Subscription instance with status "active"
#         subscription = Subscription.objects.create(status="active")

#         # Check if the is_active property returns True
#         self.assertTrue(subscription.is_active)

#         # Create a Subscription instance with status "inactive"
#         subscription = Subscription.objects.create(status="inactive")

#         # Check if the is_active property returns False
#         self.assertFalse(subscription.is_active)

#     # Test that starting a subscription with an invalid cycle raises an error
#     def test_start_subscription_with_invalid_cycle(self):
#         subscribe = Subscription.objects.create()
#         with self.assertRaises(ValueError):
#             subscribe.start_subscription("invalid_cycle")

#     # Test that a subscription can be renewed when it is expired
#     def test_renew_expired_subscription(self):
#         # Create an expired subscription
#         subscribe = Subscription.objects.create(status="expired")
#         subscribe.start_subscription("weekly")

#         # Renew the subscription
#         subscribe.renew()

#         # Assert that the subscription is now active
#         self.assertEquals(subscribe.status, "active")
#         self.assertEquals(subscribe.reason, "Subscription renewed")

#     # Test that cancelling an inactive subscription does not change its status or end date
#     def test_cancel_inactive_subscription(self):
#         # Create an inactive subscription
#         subscribe = Subscription.objects.create(status="inactive")

#         # Cancel the subscription
#         subscribe.cancel_subscription()

#         # Assert that the status and end date remain unchanged
#         self.assertEquals(subscribe.status, "inactive")
#         self.assertEquals(subscribe.end_date, datetime.date.today())

#     # Test that activating an already active subscription does not change its status or dates
#     def test_activate_active_subscription(self):
#         # Create a subscription and set its status to active
#         subscribe = Subscription.objects.create(status="active")
#         # Save the initial values
#         initial_status = subscribe.status
#         initial_end_date = subscribe.end_date
#         initial_renewal_date = subscribe.renewal_date
#         # Activate the subscription
#         subscribe.activate_subscription(30)
#         # Check that the status, end date, and renewal date remain unchanged
#         self.assertEqual(subscribe.status, initial_status)
#         self.assertEqual(subscribe.end_date, initial_end_date)
#         self.assertEqual(subscribe.renewal_date, initial_renewal_date)

#     # Test that the duration of an expired subscription can be updated successfully
#     def test_update_duration_expired_subscription(self):
#         # Create an expired subscription
#         subscribe = Subscription.objects.create(status="expired")
#         # Update the duration
#         subscribe.update_duration(30)

#         # Check if the duration is updated correctly
#         self.assertEquals(subscribe.subscription_duration, 30)

#     # Test that the search method in the Subscription class returns the correct subscriptions based on the provided query.
#     def test_search_subscription(self):
#         # Create test subscriptions
#         subscription1 = Subscription.objects.create(
#             reference="ref1",
#             reason="reason1",
#             product_type=ProductType.objects.create(name="type1"),
#         )
#         subscription2 = Subscription.objects.create(
#             reference="ref2",
#             reason="reason2",
#             product_type=ProductType.objects.create(name="type2"),
#         )
#         subscription3 = Subscription.objects.create(
#             reference="ref3",
#             reason="reason3",
#             product_type=ProductType.objects.create(name="type3"),
#         )

#         # Test search with empty query
#         result = Subscription.objects.search()
#         all_subscriptions = Subscription.objects.count()
#         self.assertEqual(len(result), all_subscriptions)
#         self.assertIn(subscription1, result)
#         self.assertIn(subscription2, result)
#         self.assertIn(subscription3, result)

#         # Test search with reference query
#         result = Subscription.objects.search(query="ref1")
#         self.assertEqual(len(result), 1)
#         self.assertIn(subscription1, result)
#         self.assertNotIn(subscription2, result)
#         self.assertNotIn(subscription3, result)

#         # Test search with reason query
#         result = Subscription.objects.search(query="reason2")
#         self.assertEqual(len(result), 1)
#         self.assertNotIn(subscription1, result)
#         self.assertIn(subscription2, result)
#         self.assertNotIn(subscription3, result)

#         # Test search with product type query
#         result = Subscription.objects.search(query="type3")
#         self.assertEqual(len(result), 1)
#         self.assertNotIn(subscription1, result)
#         self.assertNotIn(subscription2, result)
#         self.assertIn(subscription3, result)

#         # Test search with non-matching query
#         result = Subscription.objects.search(query="nonexistent")
#         self.assertEqual(len(result), 0)

#     # Test that the 'Subscription' class can filter subscriptions based on their status.
#     def test_filter_subscriptions_by_status(self):
#         # Create test subscriptions with different statuses
#         active_subscription = Subscription.objects.create(status="active")
#         inactive_subscription = Subscription.objects.create(status="inactive")
#         cancelled_subscription = Subscription.objects.create(status="cancelled")
#         expired_subscription = Subscription.objects.create(status="expired")

#         # Filter subscriptions by status
#         active_subscriptions = Subscription.objects.get_status("active")
#         inactive_subscriptions = Subscription.objects.get_status("inactive")
#         cancelled_subscriptions = Subscription.objects.get_status("cancelled")
#         expired_subscriptions = Subscription.objects.get_status("expired")

#         # Check if the correct subscriptions are returned
#         self.assertIn(active_subscription, active_subscriptions)
#         self.assertNotIn(active_subscription, inactive_subscriptions)
#         self.assertNotIn(active_subscription, cancelled_subscriptions)
#         self.assertNotIn(active_subscription, expired_subscriptions)

#         self.assertNotIn(inactive_subscription, active_subscriptions)
#         self.assertIn(inactive_subscription, inactive_subscriptions)
#         self.assertNotIn(inactive_subscription, cancelled_subscriptions)
#         self.assertNotIn(inactive_subscription, expired_subscriptions)

#         self.assertNotIn(cancelled_subscription, active_subscriptions)
#         self.assertNotIn(cancelled_subscription, inactive_subscriptions)
#         self.assertIn(cancelled_subscription, cancelled_subscriptions)
#         self.assertNotIn(cancelled_subscription, expired_subscriptions)

#         self.assertNotIn(expired_subscription, active_subscriptions)
#         self.assertNotIn(expired_subscription, inactive_subscriptions)
#         self.assertNotIn(expired_subscription, cancelled_subscriptions)
#         self.assertIn(expired_subscription, expired_subscriptions)

#     # Test that the 'get_active' method of the 'SubscriptionQueryset' returns all active subscriptions
#     def test_get_active_subscriptions(self):
#         # Create active and inactive subscriptions
#         active_subscription = Subscription.objects.create(status="active")
#         inactive_subscription = Subscription.objects.create(status="inactive")

#         # Get all active subscriptions
#         active_subscriptions = Subscription.objects.get_active()

#         # Check that only the active subscription is returned
#         self.assertEqual(len(active_subscriptions), 1)
#         self.assertEqual(active_subscriptions[0], active_subscription)

#     # Test that the 'get_started_within_week' method of the 'Subscription' class returns all subscriptions that started within the last week.
#     def test_get_subscriptions_started_within_week(self):
#         # Create subscriptions with different start dates
#         subscription1 = Subscription.objects.create(
#             start_date=datetime.date.today() - datetime.timedelta(days=8)
#         )
#         subscription2 = Subscription.objects.create(
#             start_date=datetime.date.today() - datetime.timedelta(days=6)
#         )
#         subscription3 = Subscription.objects.create(
#             start_date=datetime.date.today() - datetime.timedelta(days=5)
#         )

#         # Get subscriptions started within the last week
#         subscriptions = Subscription.objects.started_within_week()

#         # Check if the correct subscriptions are returned
#         self.assertIn(subscription2, subscriptions)
#         self.assertIn(subscription3, subscriptions)
#         self.assertNotIn(subscription1, subscriptions)

#     # Test that the 'ended_within_week' method of the 'SubscriptionQueryset' class returns all subscriptions that ended within the last week
#     def test_get_ended_within_week(self):
#         # Create a subscription that ended within the last week
#         subscription1 = Subscription.objects.create(
#             end_date=timezone.now().date() - timezone.timedelta(days=3)
#         )
#         # Create a subscription that ended more than a week ago
#         subscription2 = Subscription.objects.create(
#             end_date=timezone.now().date() - timezone.timedelta(days=10)
#         )
#         # Get all subscriptions that ended within the last week
#         subscriptions = Subscription.objects.ended_within_week()
#         # Check that the correct subscriptions are returned
#         self.assertIn(subscription1, subscriptions)
#         self.assertNotIn(subscription2, subscriptions)
