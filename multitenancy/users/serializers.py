from  rest_framework import serializers
from .models import Staff, Customer, Admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        # fields = ['id', 'first_name', 'last_name', 'username', 'email', 'type','signup_confirmation', 'avatar', 'last_login']
