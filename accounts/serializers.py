from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BankAccountType, UserBankAccount,UserAddress, UserProfile
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



class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'        
        
class UserBankAccountSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(source='account_type.name')

    class Meta:
        model = UserBankAccount
        fields = '__all__'

    def create(self, validated_data):
        if 'account_type' in validated_data:
            account_type_data = validated_data.pop('account_type')
            account_type = BankAccountType.objects.get(name=account_type_data)
        else:
            account_type = None

        user_bank_account = UserBankAccount.objects.create(
            user=self.context['request'].user,
            account_type=account_type,
            balance=0.0
        )

        return user_bank_account

