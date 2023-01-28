import unittest
from multitenancy.subscriptions.models import Plan, ProductType, Subscription

import datetime


class TestPlan(unittest.TestCase):
    
    def test_add_feature(self):
        plan = Plan.objects.create(name="basic")
        plan.add_feature("Free domain")
        features = plan.features.all()
        for feature in features:
            self.assertEquals(feature.name,"Free domain")


        self.assertEquals(plan.pk,1)
    

class TestProductType(unittest.TestCase):
    def test_create_defaults(self):
        defaults = ProductType.objects.create_defaults()
        producttypes = ProductType.objects.count()
        self.assertEquals(producttypes,3)

        
class TestSubscription(unittest.TestCase):

    def test_start_subscription(self):
        subscribe = Subscription.objects.create()
        subscribe.start_subscription("weekly")

        self.assertEquals(subscribe.status, "active")
        self.assertEquals(subscribe.cycle, "weekly")
        self.assertEquals(subscribe.reason, "Start Subscription")
        self.assertEquals(subscribe.renewal_date, datetime.date.today())
        self.assertEquals(subscribe.end_date, datetime.date.today() + datetime.timedelta(days=7))
        self.assertEquals(subscribe.subscription_duration, 7)
        

    def test_renew_subscription(self):
        subscribe = Subscription.objects.create()
        subscribe.start_subscription("weekly")
        subscribe.renew()

        self.assertEquals(subscribe.reason, "Subscription renewed")

    def test_cancel_subscription(self):
        subscribe = Subscription.objects.create()
        subscribe.start_subscription("weekly")
        subscribe.cancel_subscription()
        self.assertEquals(subscribe.end_date, datetime.date.today())
    
        self.assertEquals(subscribe.status, "cancelled")
        self.assertEquals(subscribe.reason, "Subscription cancelled")

    def test_activate_subscription(self):
        subscribe = Subscription.objects.create()
        subscribe.activate_subscription(30)

        self.assertEquals(subscribe.status, "active")
        self.assertEquals(subscribe.reason, "Subscription activated")
        self.assertEquals(subscribe.renewal_date, datetime.date.today())
        self.assertEquals(subscribe.end_date, datetime.date.today() + datetime.timedelta(days=30))

    def test_update_duration(self):
        subscribe = Subscription.objects.create()
        subscribe.update_duration(30)

        self.assertEquals(subscribe.subscription_duration, 30)

    def test_is_active(self):
        subscribe = Subscription.objects.create()
        self.assertEquals(subscribe.is_active, False)