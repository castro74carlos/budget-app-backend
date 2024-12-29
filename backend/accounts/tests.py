from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Category, Vendor
from django.urls import reverse

class UserTests(APITestCase):

    def setUp(self):
        """Set up initial data for the tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'is_staff': True,
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('user-list')  # The URL for the user list view
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Test creating a new user."""
        expected = User.objects.count() + 1
        test_data = self.user_data
        test_data['username'] = 'testuser2'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), expected)
        self.assertEqual(User.objects.get(id=response.data['id']).username, 'testuser2')

    def test_get_user(self):
        """Test retrieving a user."""
        expected = User.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected)

    def test_get_user_detail(self):
        """Test retrieving user details by ID."""
        url = reverse('user-detail', args=[self.user.id])  # URL for user detail view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        invalid_data = {'username': '', 'email': 'invalid-email'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """Test updating a user."""
        url = reverse('user-detail', args=[self.user.id])
        updated_data = {
            'username': 'updated-user',
            'email': 'updated@example.com',
            'password': 'newpassword123'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated-user')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_delete_user(self):
        """Test deleting a user."""
        url = reverse('user-detail', args=[self.user.id])
        expected = User.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), expected)

    def test_get_user_unauthorized(self):
        """Test unauthorized access."""
        # Create a new user but don't authenticate
        new_user_data = {
            'username': 'new-user',
            'email': 'new-user@example.com',
            'password': 'password456'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_user_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryTests(APITestCase):

    def setUp(self):
        """Set up initial data for the tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'is_staff': True,
        }
        self.user = User.objects.create_user(**self.user_data)
        self.category_data = {
            'name': 'test-category',
        }
        self.category = Category.objects.create(**self.category_data)
        self.url = reverse('category-list')  # The URL for the category list view
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        """Test creating a new category."""
        expected = Category.objects.count() + 1
        test_data = self.category_data
        test_data['name'] = 'test-category2'
        response = self.client.post(self.url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), expected)
        self.assertEqual(Category.objects.get(id=response.data['id']).name, 'test-category2')

    def test_get_category(self):
        """Test retrieving a category."""
        expected = Category.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected)

    def test_get_category_detail(self):
        """Test retrieving category details by ID."""
        url = reverse('category-detail', args=[self.category.id])  # URL for category detail view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test-category')

    def test_create_category_invalid_data(self):
        """Test creating a category with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category(self):
        """Test updating a category."""
        url = reverse('category-detail', args=[self.category.id])
        updated_data = {
            'name': 'updated-category',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'updated-category')

    def test_delete_category(self):
        """Test deleting a category."""
        url = reverse('category-detail', args=[self.category.id])
        expected = Category.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), expected)

    def test_get_category_unauthorized(self):
        """Test unauthorized access."""
        # Create a new category but don't authenticate
        new_category_data = {
            'name': 'new-category'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_category_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)


class VendorTests(APITestCase):

    def setUp(self):
        """Set up initial data for the tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'is_staff': True,
        }
        self.user = User.objects.create_user(**self.user_data)
        self.vendor_data = {
            'name': 'test-vendor',
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)
        self.url = reverse('vendor-list')  # The URL for the vendor list view
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_vendor(self):
        """Test creating a new vendor."""
        expected = Vendor.objects.count() + 1
        test_data = self.vendor_data
        test_data['name'] = 'test-vendor2'
        response = self.client.post(self.url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), expected)
        self.assertEqual(Vendor.objects.get(id=response.data['id']).name, 'test-vendor2')

    def test_get_vendor(self):
        """Test retrieving a vendor."""
        expected = Vendor.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected)

    def test_get_vendor_detail(self):
        """Test retrieving vendor details by ID."""
        url = reverse('vendor-detail', args=[self.vendor.id])  # URL for vendor detail view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test-vendor')

    def test_create_vendor_invalid_data(self):
        """Test creating a vendor with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_vendor(self):
        """Test updating a vendor."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        updated_data = {
            'name': 'updated-vendor',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'updated-vendor')

    def test_delete_vendor(self):
        """Test deleting a vendor."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        expected = Vendor.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), expected)

    def test_get_vendor_unauthorized(self):
        """Test unauthorized access."""
        # Create a new vendor but don't authenticate
        new_vendor_data = {
            'name': 'new-vendor'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_vendor_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

# TODO tests for accounts and transactions