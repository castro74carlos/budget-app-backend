from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user
from rest_framework import permissions, viewsets

from .models import Account, User
from .serializers import GroupSerializer, UserSerializer


@login_required
@permission_required('accounts.view_account')
def index(request):
    accounts = get_objects_for_user(
        user=request.user, 
        perms='view_account', 
        klass=Account, 
        accept_global_perms=False
    )
    
    context = {"mortgage": accounts.filter(mortgage=True)}
    
    for type in Account.AccountType:
        account_name=type.name.lower()
        account_type_key=account_name + "_accounts"
        total_type_key="total_" + account_name
        context[account_type_key] = [account for account in accounts if account.account_type==type and not account.mortgage]
        context[total_type_key] = sum_account_balances_by_type(context[account_type_key])

    return render(request, "accounts/index.html", context)

def sum_account_balances_by_type(accounts):
    return sum(account.current_balance for account in accounts)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]