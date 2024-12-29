from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Category, User, Vendor, Account, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'created', 'last_updated']

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'url', 'name', 'created', 'last_updated']

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'url',
            'name',
            'account_owner',
            'current_balance',
            'account_type',
            'latest_transaction_id',
            'mortgage',
            'created',
            'last_updated'
        ]
class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'url',
            'date',
            'vendor',
            'description',
            'amount',
            'type',
            'category',
            'account',
            'paid_off',
            'recurring',
            'created',
            'last_updated'
        ]