# Generated by Django 5.1.4 on 2024-12-17 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mortgage',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 17, 2, 50, 20, 466871)),
        ),
    ]
