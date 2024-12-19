from django.contrib import admin

from .models import Account, Category, Transaction, Vendor

class AccountAdmin(admin.ModelAdmin):
    # ...
    list_display = ["id", "name", "account_type", "last_updated", "latest_transaction_id"]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "vendor", "date", "amount", "type", "account", "category", "paid_off"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

class VendorAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)