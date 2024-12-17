from django.contrib import admin

from .models import Account

class AccountAdmin(admin.ModelAdmin):
    # ...
    list_display = ["id", "name", "account_type", "last_updated", "latest_transaction_id"]

admin.site.register(Account, AccountAdmin)