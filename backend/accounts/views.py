from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Account

@login_required
def index(request):
    accounts = Account.objects.all()
    context = {"mortgage": accounts.filter(mortgage=True)}
    
    for type in Account.AccountType:
        account_name=type.name.lower()
        account_type_key=account_name + "_accounts"
        total_type_key="total_" + account_name
        context[account_type_key] = [account for account in accounts if account.account_type==type and not account.mortgage]
        context[total_type_key] = sum_account_balances(context[account_type_key])

    return render(request, "accounts/index.html", context)

def sum_account_balances(accounts):
    return sum(account.current_balance for account in accounts)
