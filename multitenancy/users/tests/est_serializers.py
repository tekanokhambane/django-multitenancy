from rest_framework.test import APITestCase
from ..serializers import UserSerializer


class UserSerializerTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'type': 'Customer',
            'signup_confirmation': True,
            'password':'password',
        }
        self.invalid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'invalidemail',
            'type': 'Customer',
            'signup_confirmation': True,
            'password':'password',
        }

    def test_serializer_with_valid_data(self):
        serializer = UserSerializer(data=self.valid_data)# type: ignore        
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    def test_serializer_with_invalid_data(self):
        serializer = UserSerializer(data=self.invalid_data)# type: ignore
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
