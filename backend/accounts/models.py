from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from guardian.shortcuts import assign_perm

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    class AccountType(models.TextChoices):
        ASSET = 'A', 'Asset'
        CASH = 'C', 'Cash'
        DEBT = 'D', 'Debt'
        SAVINGS = 'S', 'Savings'
    
    name = models.CharField(max_length=50)
    account_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
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

    # TODO move perm assignment to serializer once DRF is implemented
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the object is new
        super().save(*args, **kwargs)  # Save the object first

        if is_new:  # Only assign permissions when the object is new
            assign_perm('change_account', self.account_owner, self)
            assign_perm('delete_account', self.account_owner, self)
            assign_perm('view_account', self.account_owner, self)

    
class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCREASE = 'INC', "Increase"
        DECREASE = 'DEC', "Decrease"

    id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
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
    recurring = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.vendor.name + " " + str(self.amount))
    