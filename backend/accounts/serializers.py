from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Category, User, Vendor


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