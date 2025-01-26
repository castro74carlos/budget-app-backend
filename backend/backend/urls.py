"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import AccountViewSet, CategoryViewSet, GroupViewSet, TransactionViewSet, UserViewSet, VendorViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls),
    path('user-accounts/', include('django.contrib.auth.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
