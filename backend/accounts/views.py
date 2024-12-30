from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.db import models
from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user
from rest_framework import permissions, viewsets

from .models import Account, Category, User, Vendor, Transaction
from .permissions import IsOwnerOrAdmin
from .serializers import CategorySerializer, GroupSerializer, UserSerializer, VendorSerializer, AccountSerializer, \
    TransactionSerializer


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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class VendorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vendors to be viewed or edited.
    """
    queryset = Vendor.objects.all().order_by('name')
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Broadly filter accounts based on user association.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return self.queryset

        # Return accounts where the user is the owner
        return self.queryset.filter(models.Q(account_owner=user)).distinct()

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """
    queryset = Transaction.objects.all().order_by('date')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Broadly filter transactions based on user association.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return self.queryset

        # Return accounts where the user is the owner
        return self.queryset.filter(models.Q(account__account_owner=user)).distinct()
