# Generated by Django 5.1.4 on 2024-12-18 04:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_account_created_alter_transaction_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]