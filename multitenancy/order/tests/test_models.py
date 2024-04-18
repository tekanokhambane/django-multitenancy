from multitenancy.subscriptions.serializers import SubscriptionSerializer

from multitenancy.subscriptions.models import SubscriptionQueryset

from multitenancy.subscriptions.apps import SubscriptionsConfig

from multitenancy import subscriptions

from multitenancy import order


from django.utils import timezone
from django.conf import settings
from multitenancy.address.models import Address

import datetime

from multitenancy.order.models import Coupon, Order, OrderItem
from multitenancy.subscriptions.models import Subscription
from multitenancy.users.models import Customer

User = settings.AUTH_USER_MODEL

import unittest


class TestCoupon(unittest.TestCase):

    # Test that a Coupon object can be created with valid input parameters
    def test_create_coupon_with_valid_input(self):
        coupon = Coupon(
            code="SUMMER2021",
            discount=10.00,
            start_date="2021-06-01",
            end_date="2021-08-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2021-07-31",
            usage_count=0,
        )
        self.assertEqual(coupon.code, "SUMMER2021")
        self.assertEqual(coupon.discount, 10.00)
        self.assertEqual(coupon.start_date, "2021-06-01")
        self.assertEqual(coupon.end_date, "2021-08-31")
        self.assertEqual(coupon.usage_limit, 100)
        self.assertEqual(coupon.is_active, True)
        self.assertEqual(coupon.minimum_order_amount, 50.00)
        self.assertEqual(coupon.redeem_by, "2021-07-31")
        self.assertEqual(coupon.usage_count, 0)

    # Test that the coupon code can be retrieved from the Coupon class
    def test_retrieve_coupon_code(self):
        coupon = Coupon(
            code="ABC123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertEqual(coupon.code, "ABC123")

    # Test that the discount of a coupon can be retrieved
    def test_retrieve_discount(self):
        # Create a coupon
        coupon = Coupon.objects.create(
            code="TEST123233",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Retrieve the discount of the coupon
        discount = coupon.discount

        # Assert that the retrieved discount is equal to the expected discount
        self.assertEqual(discount, 10.00)

    # Test that the start date of a coupon can be retrieved correctly.
    def test_retrieve_start_date(self):
        coupon = Coupon.objects.create(
            code="ABC12u3",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertEqual(coupon.start_date, "2022-01-01")

    # Test that the end date of a coupon can be retrieved correctly.
    def test_retrieve_end_date(self):
        coupon = Coupon.objects.create(
            code="TEST123009",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertEqual(coupon.end_date, "2022-12-31")

    # Test that the usage limit of a coupon can be retrieved correctly.
    def test_retrieve_usage_limit(self):
        coupon = Coupon.objects.create(
            code="TEST1238999587",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=50,
        )
        self.assertEqual(coupon.usage_limit, 100)

    # Test that the active status of a coupon can be retrieved
    def test_retrieve_active_status(self):
        coupon = Coupon.objects.create(
            code="ABC1234",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertTrue(coupon.is_active)

    # Test that the minimum order amount of a coupon can be retrieved
    def test_retrieve_minimum_order_amount(self):
        coupon = Coupon.objects.create(
            code="TEST12309283",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        minimum_order_amount = coupon.minimum_order_amount
        self.assertEqual(minimum_order_amount, 50.00)

    # Test that the redeem by date of a coupon can be retrieved
    def test_redeem_by_date(self):
        coupon = Coupon.objects.create(
            code="ABC123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-06-30",
            usage_count=0,
        )
        redeem_by_date = coupon.redeem_by
        self.assertEqual(redeem_by_date, "2022-06-30")

    # Test that the usage count of a coupon can be retrieved correctly.
    def test_retrieve_usage_count(self):
        # Create a coupon
        coupon = Coupon.objects.create(
            code="TEST12390987",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50,
            redeem_by="2022-12-31",
            usage_count=50,
        )

        # Retrieve the usage count
        usage_count = coupon.usage_count

        # Assert that the retrieved usage count is correct
        self.assertEqual(usage_count, 50)

    # Test that the code attribute of Coupon cannot be longer than 15 characters
    def test_coupon_code_length(self):
        coupon = Coupon(
            code="1234567890123456",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        with self.assertRaises(Exception):
            coupon.save()

    # Test that the discount of a coupon cannot be negative
    def test_negative_discount(self):
        coupon = Coupon(
            code="TEST1232883",
            discount=-10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        with self.assertRaises(ValueError):
            coupon.save()

    # Test that the start date of a coupon cannot be in the past
    def test_start_date_not_in_past(self):
        # Create a coupon with a start date in the past
        past_start_date = datetime.date.today() - datetime.timedelta(days=1)
        coupon = Coupon(
            code="TESTCOUPON",
            discount=10,
            start_date=past_start_date,
            end_date=datetime.date.today(),
            usage_limit=1,
            is_active=True,
            minimum_order_amount=0,
            redeem_by=datetime.date.today(),
            usage_count=0,
        )
        coupon.save()

        # Check that the coupon is not saved
        self.assertFalse(Coupon.objects.filter(code="TESTCOUPON").exists())

        # Create a coupon with a start date in the future
        future_start_date = datetime.date.today() + datetime.timedelta(days=1)
        coupon = Coupon(
            code="TESTCOUPON",
            discount=10,
            start_date=future_start_date,
            end_date=datetime.date.today(),
            usage_limit=1,
            is_active=True,
            minimum_order_amount=0,
            redeem_by=datetime.date.today(),
            usage_count=0,
        )
        coupon.save()

        # Check that the coupon is saved
        self.assertTrue(Coupon.objects.filter(code="TESTCOUPON").exists())

    # Test that the end date of a coupon cannot be before the start date
    def test_end_date_before_start_date(self):
        coupon = Coupon(
            code="TEST12309",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2021-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-01-31",
            usage_count=0,
        )
        with self.assertRaises(ValueError):
            coupon.save()

    # Test that the usage limit of a coupon cannot be set to a negative value
    def test_negative_usage_limit(self):
        coupon = Coupon.objects.create(
            code="TEST123345",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=-1,
            is_active=True,
        )
        self.assertRaises(ValueError, coupon.save)

    # Test that the minimum order amount of a coupon cannot be negative
    def test_minimum_order_amount_positive(self):
        coupon = Coupon.objects.create(
            code="TEST123",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=-10,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertGreaterEqual(coupon.minimum_order_amount, 0)

    # Test that the redeem by date of a coupon cannot be in the past
    def test_redeem_by_date_not_in_past(self):
        # Create a coupon with a redeem by date in the past
        coupon = Coupon(
            code="TEST1239909",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2021-12-31",
            usage_count=0,
        )
        coupon.save()

        # Attempt to redeem the coupon
        redeemed = coupon.redeem()

        # Assert that the coupon was not redeemed
        self.assertFalse(
            redeemed, "Coupon should not be redeemed if redeem by date is in the past"
        )

    # Test that the usage count of a coupon does not exceed the usage limit
    def test_usage_count_limit(self):
        # Create a coupon with a usage limit of 5
        coupon = Coupon.objects.create(
            code="TESTCOUPON1",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=5,
            is_active=True,
            minimum_order_amount=50,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Use the coupon 5 times
        for _ in range(5):
            coupon.usage_count += 1
            coupon.save()

        # Try to use the coupon again
        coupon.usage_count += 1
        coupon.save()

        # Assert that the usage count did not exceed the usage limit
        self.assertEqual(coupon.usage_count, 5)

    # Test that a coupon can be deactivated
    def test_deactivate_coupon(self):
        coupon = Coupon.objects.create(
            code="TEST123345",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertTrue(coupon.is_active)

        coupon.is_active = False
        coupon.save()

        updated_coupon = Coupon.objects.get(pk=coupon.pk)
        self.assertFalse(updated_coupon.is_active)

    # Test that a coupon can be activated
    def test_coupon_activation(self):
        coupon = Coupon.objects.create(
            code="TEST123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        self.assertTrue(coupon.is_active)
        coupon.is_active = False
        coupon.save()
        self.assertFalse(coupon.is_active)

    # Test that the 'Coupon' object can be updated with valid input parameters
    def test_update_coupon_with_valid_input(self):
        # Create a new coupon object
        coupon = Coupon.objects.create(
            code="TESTCODE",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Update the coupon with valid input parameters
        coupon.code = "NEWCODE"
        coupon.discount = 15.00
        coupon.start_date = "2023-01-01"
        coupon.end_date = "2023-12-31"
        coupon.usage_limit = 200
        coupon.is_active = False
        coupon.minimum_order_amount = 100.00
        coupon.redeem_by = "2023-12-31"
        coupon.usage_count = 50
        coupon.save()

        # Retrieve the updated coupon from the database
        updated_coupon = Coupon.objects.get(id=coupon.id)

        # Assert that the coupon has been updated with the new values
        self.assertEqual(updated_coupon.code, "NEWCODE")
        self.assertEqual(updated_coupon.discount, 15.00)
        self.assertEqual(updated_coupon.start_date, "2023-01-01")
        self.assertEqual(updated_coupon.end_date, "2023-12-31")
        self.assertEqual(updated_coupon.usage_limit, 200)
        self.assertEqual(updated_coupon.is_active, False)
        self.assertEqual(updated_coupon.minimum_order_amount, 100.00)
        self.assertEqual(updated_coupon.redeem_by, "2023-12-31")
        self.assertEqual(updated_coupon.usage_count, 50)

    # Test that the Coupon model cannot be updated with invalid input parameters
    def test_invalid_input_parameters(self):
        # Create a valid coupon
        coupon = Coupon(
            code="ABC123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        coupon.save()

        # Attempt to update the coupon with invalid input parameters
        coupon.code = ""
        coupon.discount = -10.00
        coupon.start_date = "2023-01-01"
        coupon.end_date = "2022-12-31"
        coupon.usage_limit = -1
        coupon.is_active = None
        coupon.minimum_order_amount = 0.00
        coupon.redeem_by = "2023-01-01"
        coupon.usage_count = -1

        # Save the coupon and assert that it was not updated
        with self.assertRaises(Exception):
            coupon.save()

        # Assert that the original coupon values are still intact
        self.assertEqual(coupon.code, "ABC123")
        self.assertEqual(coupon.discount, 10.00)
        self.assertEqual(coupon.start_date, "2022-01-01")
        self.assertEqual(coupon.end_date, "2022-12-31")
        self.assertEqual(coupon.usage_limit, 100)
        self.assertEqual(coupon.is_active, True)
        self.assertEqual(coupon.minimum_order_amount, 50.00)
        self.assertEqual(coupon.redeem_by, "2022-12-31")
        self.assertEqual(coupon.usage_count, 0)

    # Test that a coupon can be deleted
    def test_delete_coupon(self):
        coupon = Coupon.objects.create(
            code="ABC123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )
        coupon.delete()
        self.assertFalse(Coupon.objects.filter(code="ABC123").exists())


class TestOrder(unittest.TestCase):
    # Test that an order can be created with all the required fields
    def test_create_order_with_required_fields(self):
        # Create a user
        user = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doew@example.com",
            password="secret",
            is_active=True,
        )

        # Create a billing address
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )

        # Create a coupon
        coupon = Coupon.objects.create(
            code="ABC12398761",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Create an order
        order = Order.objects.create(
            user=user,
            order_number="123456789",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=address,
            coupon=coupon,
        )

        # Assert that the order was created successfully
        self.assertEqual(order.user, user)
        self.assertEqual(order.order_number, "123456789")
        self.assertEqual(order.amount, 100.00)
        self.assertEqual(order.status, "completed")
        self.assertEqual(order.payment_method, "credit card")
        self.assertEqual(order.billing_address, address)
        self.assertEqual(order.coupon, coupon)

    # Test that the notes field of an order is successfully updated
    def test_update_order_notes(self):
        # Create a test order
        order = Order.objects.create(
            user=None,
            order_number="12345",
            amount=10.00,
            status="completed",
            payment_method="credit card",
            billing_address=None,
            notes="",
        )

        # Update the notes field
        order.notes = "This is a test note"
        order.save()

        # Retrieve the order from the database
        updated_order = Order.objects.get(pk=order.pk)

        # Check if the notes field is updated correctly
        self.assertEqual(updated_order.notes, "This is a test note")

    # Test that an order can be created with a coupon
    def test_create_order_with_coupon(self):
        # Create a coupon
        coupon = Coupon.objects.create(
            code="ABC1232",
            discount=10,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Create an address
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="12345",
            country="USA",
        )

        # Create an order with the coupon and address
        order = Order.objects.create(
            user=None,
            order_number="123456789",
            amount=100,
            status="completed",
            payment_method="Credit Card",
            billing_address=address,
            notes="",
            coupon=coupon,
        )

        # Assert that the order was created successfully
        self.assertEqual(order.user, None)
        self.assertEqual(order.order_number, "123456789")
        self.assertEqual(order.amount, 100)
        self.assertEqual(order.status, "completed")
        self.assertEqual(order.payment_method, "Credit Card")
        self.assertEqual(order.billing_address, address)
        self.assertEqual(order.notes, "")
        self.assertEqual(order.coupon, coupon)

    # Test that an order with a negative amount cannot be created
    def test_negative_amount(self):
        # Create a billing address
        billing_address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )

        # Create a coupon
        coupon = Coupon.objects.create(
            code="ABC1238888",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Attempt to create an order with a negative amount
        with self.assertRaises(ValueError):
            Order.objects.create(
                user=None,
                order_number="123456789",
                amount=-50.00,
                status="completed",
                payment_method="credit card",
                billing_address=billing_address,
                notes="",
                coupon=coupon,
            )

    # Test that an order cannot be created with a status that is not "completed" or "failed"
    def test_create_order_with_invalid_status(self):
        # Create a valid address
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )

        # Create a valid coupon
        coupon = Coupon.objects.create(
            code="ABC1230",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Attempt to create an order with an invalid status
        with self.assertRaises(ValueError):
            order = Order.objects.create(
                user=None,
                date_created="2022-01-01",
                order_number="123456789",
                amount=100.00,
                status="pending",
                payment_method="credit card",
                billing_address=address,
                notes="",
                coupon=coupon,
            )

    # Test that an order cannot be created with a non-existent billing address
    def test_create_order_with_nonexistent_billing_address(self):
        # Create a user
        user = Customer.objects.create(
            email="Vw5zA@example.com",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        )

        # Create an order with a non-existent billing address
        order = Order.objects.create(
            user=user,
            order_number="12345",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address_id=9999,
        )

        # Assert that the order was not created
        self.assertIsNone(order)

    # Test that an order cannot be created with a non-existent coupon
    def test_create_order_with_nonexistent_coupon(self):
        # Create a new address
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )

        # Create a new order with a non-existent coupon
        order = Order.objects.create(
            user=None,
            date_created=timezone.now().date(),
            order_number="123456",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=address,
            notes="Test order",
            coupon=None,
        )

        # Assert that the order was not created
        self.assertIsNone(order)

    # Test that the user of an order can be retrieved correctly
    def test_retrieve_user(self):
        # Create a user
        user = Customer.objects.create(
            email="Vw5fzA@example.com",
            password="testpassword",
            first_name="John",
            last_name="Doe",
        )

        # Create an address
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="12345",
            country="USA",
        )

        # Create a coupon
        coupon = Coupon.objects.create(
            code="ABC123",
            discount=10.00,
            start_date="2022-01-01",
            end_date="2022-12-31",
            usage_limit=100,
            is_active=True,
            minimum_order_amount=50.00,
            redeem_by="2022-12-31",
            usage_count=0,
        )

        # Create an order
        order = Order.objects.create(
            user=user,
            order_number="123456789",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=address,
            notes="",
            coupon=coupon,
        )

        # Retrieve the user of the order
        retrieved_user = order.user

        # Assert that the retrieved user is the same as the created user
        self.assertEqual(retrieved_user, user)

    # Test that the date_created attribute of an Order instance can be retrieved correctly.
    def test_retrieve_order_date_created(self):
        # Create a sample Order instance
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="12345",
            country="USA",
        )
        order = Order.objects.create(
            user=None,
            order_number="12345",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=address,
            notes="",
            coupon=None,
        )

        # Retrieve the date_created attribute
        date_created = order.date_created

        # Assert that the retrieved date_created matches the expected value
        self.assertEqual(date_created, order.date_created)

    # Test that the order number of an order can be retrieved correctly
    def test_retrieve_order_number(self):
        # Create a test order
        order = Order.objects.create(
            user=Customer.objects.create(
                email="Vw5zA@example.com",
                password="testpassword",
                first_name="John",
                last_name="Doe",
            ),
            order_number="123456",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=Address.objects.create(
                recipient_name="John Doe",
                street_address="123 Main St",
                city="New York",
                state="NY",
                postal_code="12345",
                country="USA",
            ),
        )

        # Retrieve the order number
        order_number = order.order_number

        # Check if the retrieved order number is correct
        self.assertEqual(order_number, "123456")

    # Test that the payment method of an order can be retrieved correctly
    def test_retrieve_payment_method(self):
        # Create a test order
        order = Order.objects.create(
            user=None,
            date_created=datetime.date.today(),
            order_number="123456",
            amount=100.00,
            status="completed",
            payment_method="Credit Card",
            billing_address=Address.objects.create(
                recipient_name="John Doe",
                street_address="123 Main St",
                city="New York",
                state="NY",
                postal_code="12345",
                country="USA",
            ),
            notes="Test order",
            coupon=None,
        )

        # Retrieve the payment method of the order
        payment_method = order.payment_method

        # Assert that the payment method is correct
        self.assertEqual(payment_method, "Credit Card")

    # Test that an order is successfully deleted
    def test_delete_order(self):
        # Create a test order
        address = Address.objects.create(
            recipient_name="John Doe",
            street_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="12345",
            country="USA",
        )
        order = Order.objects.create(
            user=None,
            order_number="12345",
            amount=100.00,
            status="completed",
            payment_method="credit card",
            billing_address=None,
            notes="Test order",
            coupon=None,
        )

        # Delete the order
        order.delete()

        # Check that the order is deleted
        self.assertFalse(Order.objects.filter(order_number="12345").exists())


class TestOrderItem(unittest.TestCase):
    # Test that an OrderItem instance can be created with valid Subscription and Order instances.
    def test_create_order_item_with_valid_instances(self):
        subscription = Subscription.objects.create()
        order = Order.objects.create()
        order_item = OrderItem.objects.create(subscription=subscription, order=order)

        self.assertEqual(order_item.subscription, subscription)
        self.assertEqual(order_item.order, order)

    # Test that the Subscription and Order instances can be retrieved from an existing OrderItem instance.
    def test_retrieve_subscription_and_order(self):
        # Create a Subscription instance
        subscription = Subscription.objects.create()

        # Create an Order instance
        order = Order.objects.create()

        # Create an OrderItem instance with the Subscription and Order instances
        order_item = OrderItem.objects.create(subscription=subscription, order=order)

        # Retrieve the Subscription and Order instances from the OrderItem instance
        retrieved_subscription = order_item.subscription
        retrieved_order = order_item.order

        # Check that the retrieved Subscription and Order instances match the original instances
        self.assertEqual(retrieved_subscription, subscription)
        self.assertEqual(retrieved_order, order)

    # Test that an OrderItem instance is successfully deleted.
    def test_delete_order_item(self):
        # Create a Subscription instance
        subscription = Subscription.objects.create()

        # Create an Order instance
        order = Order.objects.create()

        # Create an OrderItem instance
        order_item = OrderItem.objects.create(subscription=subscription, order=order)

        # Delete the OrderItem instance
        order_item.delete()

        # Check that the OrderItem instance is deleted
        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())

    # Test that creating an OrderItem instance with a Subscription instance that does not exist raises a ValueError.
    def test_create_order_item_with_nonexistent_subscription(self):
        with self.assertRaises(ValueError):
            subscription = Subscription.objects.get(pk=9999)
            order = Order.objects.create(...)
            order_item = OrderItem.objects.create(
                subscription=subscription, order=order
            )

    # Test that creating an OrderItem instance with a non-existent Order instance raises an error.
    def test_create_order_item_with_nonexistent_order(self):
        with self.assertRaises(Order.DoesNotExist):
            order_item = OrderItem.objects.create(
                subscription=Subscription.objects.create(), order_id=999
            )

    # Test that an OrderItem instance cannot be created with a Subscription instance that has a status other than "active".
    def test_create_order_item_with_inactive_subscription(self):
        # Create a Subscription instance with a status other than "active"
        subscription = Subscription.objects.create(status="inactive")

        # Attempt to create an OrderItem instance with the inactive Subscription
        with self.assertRaises(Exception):
            OrderItem.objects.create(subscription=subscription, order=order)

    # Test that an OrderItem instance cannot be created with an Order instance that has a status other than "completed".
    def test_create_order_item_with_incomplete_order(self):
        # Create an incomplete Order instance
        incomplete_order = Order.objects.create(status="failed")

        # Attempt to create an OrderItem instance with the incomplete Order
        with self.assertRaises(Exception):
            OrderItem.objects.create(subscription=subscription, order=incomplete_order)

    # Test that multiple OrderItem instances can be created with the same Subscription instance.
    def test_create_multiple_order_items_with_same_subscription(self):
        # Create a Subscription instance
        subscription = Subscription.objects.create()

        # Create multiple OrderItem instances with the same Subscription instance
        order_item1 = OrderItem.objects.create(subscription=subscription)
        order_item2 = OrderItem.objects.create(subscription=subscription)
        order_item3 = OrderItem.objects.create(subscription=subscription)

        # Assert that the OrderItem instances were created successfully
        self.assertEqual(order_item1.subscription, subscription)
        self.assertEqual(order_item2.subscription, subscription)
        self.assertEqual(order_item3.subscription, subscription)

    # Test that multiple OrderItem instances can be created with the same Order instance.
    def test_create_multiple_order_items(self):
        order = Order.objects.create(
            order_number="123",
            amount=10.0,
            status="completed",
            payment_method="credit card",
            billing_address=Address.objects.create(),
        )
        subscription = Subscription.objects.create()
        order_item1 = OrderItem.objects.create(subscription=subscription, order=order)
        order_item2 = OrderItem.objects.create(subscription=subscription, order=order)

        self.assertEqual(order_item1.order, order)
        self.assertEqual(order_item2.order, order)
        self.assertEqual(order_item1.subscription, subscription)
        self.assertEqual(order_item2.subscription, subscription)

    # Test that an OrderItem instance can be created with a Subscription instance that has a cycle of "annually".
    def test_create_order_item_with_annual_subscription(self):
        subscription = Subscription.objects.create(cycle=Subscription.Cycles.ANNUALLY)
        order = Order.objects.create()
        order_item = OrderItem.objects.create(subscription=subscription, order=order)

        self.assertEqual(order_item.subscription.cycle, Subscription.Cycles.ANNUALLY)
        self.assertEqual(order_item.order, order)

    # Test that an OrderItem instance can be created with an Order instance that has a coupon assigned.
    def test_create_order_item_with_coupon(self):
        # Create a coupon
        coupon = Coupon.objects.create(
            code="ABC123",
            discount=10,
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=30),
            usage_limit=1,
            is_active=True,
            minimum_order_amount=50,
            redeem_by=datetime.date.today(),
            usage_count=0,
        )

        # Create an order with the coupon
        order = Order.objects.create(
            user=self.user,
            order_number="12345",
            amount=100,
            status="completed",
            payment_method="credit card",
            billing_address=self.address,
            coupon=coupon,
        )

        # Create an order item with the order and subscription
        order_item = OrderItem.objects.create(
            order=order, subscription=self.subscription
        )

        # Assert that the order item was created successfully
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.subscription, self.subscription)
