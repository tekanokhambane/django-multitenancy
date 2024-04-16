from django.test import TestCase
import json
import datetime
from ..models import Plan, ProductFeature,ProductType, Subscription
from ..serializers import PlanSerialiser, ProductFeatureSerializer, ProductTypeSerializer, SubscriptionSerializer

import json

class PlanSerializerTestCase(TestCase):

    def setUp(self):
        self.product_feature_1 = ProductFeature.objects.create(
            name='Feature 1'
        )
        self.product_feature_2 = ProductFeature.objects.create(
            name='Feature 2'
        )
        self.plan = Plan.objects.create(
            name='Plan 1',
            description='Plan 1 description',
            price=100.0,
        )
        self.plan.features.add(self.product_feature_1, self.product_feature_2)

    def test_plan_serializer(self):
        #plan = Plan.objects.get(id=self.plan.id)
        serialized_data = PlanSerialiser(self.plan).data
        deserialized_data = json.loads(json.dumps(serialized_data))
        self.assertEqual(self.plan.pk, deserialized_data['id'])
        self.assertEqual(self.plan.name, deserialized_data['name'])
        self.assertEqual(self.plan.description, deserialized_data['description'])
        self.assertEqual(self.plan.price, float(deserialized_data['price']))
        # Convert QuerySet to list of dictionaries
        actual_fueatures_data = list(self.plan.features.all().values('id', 'name'))
        self.assertEqual(actual_fueatures_data, deserialized_data['features'])
        # for feature in self.plan.features.all():
        #     self.assertEqual(feature.id, serialized_data)
            

class ProductFeatureSerializerTestCase(TestCase):

    def setUp(self):
        self.product_feature = ProductFeature.objects.create(
            name='Feature 1'
        )

    def test_product_feature_serializer(self):
        feature = ProductFeature.objects.get(id=self.product_feature.pk)
        serializer = ProductFeatureSerializer(feature)
        serialized_data = json.dumps(serializer.data)
        self.assertIn('"id": {}'.format(feature.pk), serialized_data)
        self.assertIn('"name": "{}"'.format(feature.name), serialized_data)


class ProductTypeSerializerTestCase(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            name='Type 1'
        )

    def test_product_type_serializer(self):
        type = ProductType.objects.get(id=self.product_type.id)
        serializer = ProductTypeSerializer(type)
        serialized_data = json.dumps(serializer.data)
        self.assertIn('"id": {}'.format(type.id), serialized_data)
        self.assertIn('"name": "{}"'.format(type.name), serialized_data)

class SubscriptionSerializerTestCase(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            name='Type 1'
        )
        self.subscription = Subscription.objects.create(
            cycle="monthly",
            subscription_duration=1,
            end_date=datetime.date.today() + datetime.timedelta(days=30),
            renewal_date=datetime.date.today() + datetime.timedelta(days=30),
            reference='123456789',
            last_updated=datetime.datetime.now(),
            product_type=self.product_type,
            reason='Test reason',
            status="active",
        )

    def test_subscription_serializer(self):
        subscription = Subscription.objects.get(id=self.subscription.id)
        #serializer = SubscriptionSerializer(subscription)
        # serialized_data = json.dumps(serializer.data)
        serialized_data = SubscriptionSerializer(self.subscription).data
        deserialized_data = json.loads(json.dumps(serialized_data))
        start_date = self.subscription.start_date
        end_date = self.subscription.end_date
        self.assertEqual(self.subscription.id, deserialized_data['id'])
        self.assertEqual(self.subscription.cycle, deserialized_data['cycle'])
        self.assertEqual(self.subscription.subscription_duration, deserialized_data['subscription_duration'])
        self.assertEqual(start_date.strftime('%Y-%m-%d')  , deserialized_data['start_date'])
        self.assertEqual(end_date.strftime('%Y-%m-%d'), deserialized_data['end_date'])
        self.assertEqual(self.subscription.created_date.strftime('%Y-%m-%d'), deserialized_data['created_date'])
        self.assertEqual(self.subscription.renewal_date.strftime('%Y-%m-%d'), deserialized_data['renewal_date'])
        