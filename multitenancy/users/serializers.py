from  rest_framework import serializers
from .models import Staff, Customer, Admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
      
