from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BankAccountType, UserBankAccount
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': False},
            'email': {'required': False},
        }







class BankAccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountType
        fields = '__all__'

class UserBankAccountSerializer(serializers.ModelSerializer):
    account_type = BankAccountTypeSerializer()

    class Meta:
        model = UserBankAccount
        fields = '__all__'        