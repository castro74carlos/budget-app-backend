# Generated by Django 5.1.4 on 2024-12-18 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_vendor_transaction_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
    ]