from datetime import datetime
from django.db import models

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


    # id is auto, only change if expecting id numbers to be large, see below:
    # id = models.BigAutoField(primary_key=True)  # Explicit primary key
    
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
    created = models.DateTimeField(default=datetime.now())
    last_updated = models.DateTimeField(auto_now=True)
    latest_transaction_id = models.BigIntegerField(default=0)
    mortgage = models.BooleanField(default=False)
    # interest_rate
    # promo_period
    


