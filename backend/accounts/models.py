from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    class AccountHolder(models.TextChoices):
        HANNAH = 'HK', 'Hannah'
        CARLOS = 'CC', 'Carlos'
        JOINT = 'J', 'Joint Account'

    class AccountType(models.TextChoices):
        ASSET = 'A', 'Asset'
        CASH = 'C', 'Cash'
        DEBT = 'D', 'Debt'
        SAVINGS = 'S', 'Savings'
    
    name = models.CharField(max_length=50)
    account_holder = models.CharField(
        max_length=2,
        choices=AccountHolder
    )
    current_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    account_type = models.CharField(
        max_length=2,
        choices=AccountType,
    )
    latest_transaction_id = models.BigIntegerField(null=True, blank=True)
    mortgage = models.BooleanField(default=False)
    # interest_rate 
    # promo_period
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCREASE = 'INC', "Increase"
        DECREASE = 'DEC', "Decrease"

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    type = models.CharField(
        max_length=3,
        choices=TransactionType
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    paid_off = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
