from django.contrib import admin

from .models import Account, Category, Transaction

class AccountAdmin(admin.ModelAdmin):
    # ...
    list_display = ["id", "name", "account_type", "last_updated", "latest_transaction_id"]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "date", "amount", "type", "account", "category"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)