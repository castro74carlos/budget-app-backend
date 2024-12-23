from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user
from .models import Account

@login_required
@permission_required('accounts.view_account')
def index(request):
    accounts = get_objects_for_user(
        user=request.user, 
        perms='view_account', 
        klass=Account, 
        accept_global_perms=False
    )
    print(accounts)
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
