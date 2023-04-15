
import random
from django.contrib.auth.models import AbstractUser

from django.db import models

from .constants import GENDER_CHOICE
from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=75)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} {self.email}"

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0
    



class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    
    def create(self, validated_data):
       account_type_data = validated_data.pop('account_type')['name']
       account_type = BankAccountType.objects.get(name=account_type_data)
    
       user_bank_account = UserBankAccount.objects.create(
          user=self.context['request'].user,
          account_type=account_type,
          balance=0.0
       )

       return user_bank_account
    
    def __str__(self):
        return self.name

    


import random

class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.account_no} {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.account_no:
            # If account_no is not set, generate a random 10-digit number
            while True:
                account_no = random.randint(10**9, 10**10-1)
                if not UserBankAccount.objects.filter(account_no=account_no).exists():
                    self.account_no = account_no
                    break
        super().save(*args, **kwargs)

   


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.username
    

class UserProfile(models.Model):
    user_bank_account = models.OneToOneField(
        UserBankAccount,
        related_name='user_profile',
        on_delete=models.CASCADE,
    )
    user_address = models.OneToOneField(
        UserAddress,
        related_name='user_profile',
        on_delete=models.CASCADE,
    )
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image= models.ImageField('resim',blank=True,null=True,upload_to="media/")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

