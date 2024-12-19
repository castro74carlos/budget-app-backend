# Generated by Django 5.1.4 on 2024-12-17 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 17, 2, 1, 46, 809400)),
        ),
        migrations.AlterField(
            model_name='account',
            name='latest_transaction_id',
            field=models.BigIntegerField(default=0),
        ),
    ]