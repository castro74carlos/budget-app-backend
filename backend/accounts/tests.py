from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Category, Vendor, Account, Transaction
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
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected, User.objects.count())
        self.assertEqual('testuser2', User.objects.get(id=response.data['id']).username)

    def test_get_user(self):
        """Test retrieving a user."""
        expected = User.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data['count'])

    def test_get_user_detail(self):
        """Test retrieving user details by ID."""
        url = reverse('user-detail', args=[self.user.id])  # URL for user detail view
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('testuser', response.data['username'])

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        invalid_data = {'username': '', 'email': 'invalid-email'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_user(self):
        """Test updating a user."""
        url = reverse('user-detail', args=[self.user.id])
        updated_data = {
            'username': 'updated-user',
            'email': 'updated@example.com',
            'password': 'newpassword123'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual('updated-user', self.user.username)
        self.assertEqual('updated@example.com', self.user.email)

    def test_delete_user(self):
        """Test deleting a user."""
        url = reverse('user-detail', args=[self.user.id])
        expected = User.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected, User.objects.count())

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
        self.assertEqual(status.HTTP_403_FORBIDDEN, unauthorized_response.status_code)


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
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected, Category.objects.count())
        self.assertEqual('test-category2', Category.objects.get(id=response.data['id']).name)

    def test_get_category(self):
        """Test retrieving a category."""
        expected = Category.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data['count'])

    def test_get_category_detail(self):
        """Test retrieving category details by ID."""
        url = reverse('category-detail', args=[self.category.id])  # URL for category detail view
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('test-category', response.data['name'])

    def test_create_category_invalid_data(self):
        """Test creating a category with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_category(self):
        """Test updating a category."""
        url = reverse('category-detail', args=[self.category.id])
        updated_data = {
            'name': 'updated-category',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category.refresh_from_db()
        self.assertEqual('updated-category', self.category.name)

    def test_delete_category(self):
        """Test deleting a category."""
        url = reverse('category-detail', args=[self.category.id])
        expected = Category.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected, Category.objects.count())

    def test_get_category_unauthorized(self):
        """Test unauthorized access."""
        # Create a new category but don't authenticate
        new_category_data = {
            'name': 'new-category'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_category_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, unauthorized_response.status_code)


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
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected, Vendor.objects.count())
        self.assertEqual('test-vendor2', Vendor.objects.get(id=response.data['id']).name)

    def test_get_vendor(self):
        """Test retrieving a vendor."""
        expected = Vendor.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data['count'])

    def test_get_vendor_detail(self):
        """Test retrieving vendor details by ID."""
        url = reverse('vendor-detail', args=[self.vendor.id])  # URL for vendor detail view
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('test-vendor', response.data['name'])

    def test_create_vendor_invalid_data(self):
        """Test creating a vendor with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_vendor(self):
        """Test updating a vendor."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        updated_data = {
            'name': 'updated-vendor',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.vendor.refresh_from_db()
        self.assertEqual('updated-vendor', self.vendor.name)

    def test_delete_vendor(self):
        """Test deleting a vendor."""
        url = reverse('vendor-detail', args=[self.vendor.id])
        expected = Vendor.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected, Vendor.objects.count())

    def test_get_vendor_unauthorized(self):
        """Test unauthorized access."""
        # Create a new vendor but don't authenticate
        new_vendor_data = {
            'name': 'new-vendor'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_vendor_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, unauthorized_response.status_code)


class AccountTests(APITestCase):

    def setUp(self):
        """Set up initial data for the tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'is_staff': False,
        }
        self.user = User.objects.create_user(**self.user_data)
        user2_data = self.user_data
        user2_data['name'] =  'testuser2'
        self.user2 = User.objects.create_user(user2_data)
        self.account_data = {
            'name': 'test-account',
            'account_owner': self.user,
            'current_balance': 30.00,
            'account_type': 'C',
        }
        self.account = Account.objects.create(**self.account_data)
        account2_data = self.account_data
        account2_data['account_owner'] = self.user2
        self.account2 = Account.objects.create(**account2_data)
        self.url = reverse('account-list')  # The URL for the account list view
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_account(self):
        """Test creating a new account."""
        expected = Account.objects.count() + 1
        test_data = self.account_data
        test_data['name'] = 'test-account2'
        test_data['account_owner'] = str(self.user.id)
        response = self.client.post(self.url, test_data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected, Account.objects.count())
        self.assertEqual('test-account2', Account.objects.get(id=response.data['id']).name)

    def test_create_account_for_other_user(self):
        """Test creating a new account for a different user."""
        test_data = self.account_data
        test_data['name'] = 'test-account2'
        test_data['account_owner'] = str(self.user2.id)
        response = self.client.post(self.url, test_data, format='json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_account(self):
        """Test retrieving an account."""
        expected = Account.objects.filter(account_owner=self.user).count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.data['count'])

    def test_get_account_detail(self):
        """Test retrieving account details by ID."""
        url = reverse('account-detail', args=[self.account.id])  # URL for account detail view
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('test-account', response.data['name'])

    def test_create_account_invalid_data(self):
        """Test creating an account with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_account(self):
        """Test updating an account."""
        url = reverse('account-detail', args=[self.account.id])
        updated_data = {
            'name': 'updated-account',
            'account_owner': self.user.id,
            'current_balance': 30.0,
            'account_type': "C"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.account.refresh_from_db()
        self.assertEqual('updated-account', self.account.name)

    def test_update_account_owner_to_other_user(self):
        """Test updating an account."""
        url = reverse('account-detail', args=[self.account.id])
        updated_data = {
            'name': 'updated-account',
            'account_owner': self.user2.id,
            'current_balance': 30.0,
            'account_type': "C"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_account(self):
        """Test deleting an account."""
        url = reverse('account-detail', args=[self.account.id])
        expected = Account.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected, Account.objects.count())

    def test_get_account_unauthorized(self):
        """Test unauthorized access."""
        # Create a new account but don't authenticate
        new_account_data = {
            'name': 'new-account'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_account_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, unauthorized_response.status_code)

class TransactionTests(APITestCase):

    def setUp(self):
        """Set up initial data for the tests."""
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'is_staff': False,
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category_data = {
            'name': 'test-category',
        }
        self.category1 = self.client.post(reverse('category-list'), self.category_data, format='json').data
        self.vendor_data = {
            'name': 'test-vendor',
        }
        self.vendor1 = self.client.post(reverse('vendor-list'), self.vendor_data, format='json').data

        self.userJson = self.client.get(reverse('user-detail', args=[self.user.id])).data
        self.account_data = {
            'name': 'test-account',
            'account_owner': self.user.id,
            'current_balance': 30.00,
            'account_type': 'C',
        }
        self.account = self.client.post(reverse('account-list'), self.account_data, format='json').data
        self.user2_data = self.user_data
        self.user2_data['username'] = 'test-user-alt'
        self.user2_data['is_staff'] = False
        self.user2 = User.objects.create_user(**self.user2_data)
        account2_data = self.account_data
        account2_data['account_owner'] = self.user2
        self.account2 = Account.objects.create(**account2_data)
        self.transaction_data = {
            'date': '2024-02-14',
            'vendor': self.vendor1['url'],
            'description': 'vendor item',
            'amount': 30.0,
            'type': 'INC',
            'category': self.category1['url'],
            'account': self.account['url']
        }
        self.url = reverse('transaction-list')  # The URL for the transaction list view
        self.transaction = self.client.post(self.url, self.transaction_data, format='json').data


    def test_create_transaction(self):
        """Test creating a new transaction."""
        expected = Transaction.objects.count() + 1
        test_data = self.transaction_data
        test_data['description'] = 'test-transaction2'
        response = self.client.post(self.url, test_data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected, Transaction.objects.count())
        self.assertEqual('test-transaction2', Transaction.objects.get(id=response.data['id']).description)

    def test_create_transaction_for_unauthorized_account(self):
        """Test creating a new transaction for a different user."""
        test_data = self.transaction_data
        test_data['description'] = 'test-transaction2'
        test_data['account'] = 'somehost.com/' + str(self.account2.id) + '/'
        response = self.client.post(self.url, test_data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_transaction(self):
        """Test retrieving a transaction."""
        expected = Transaction.objects.filter(account=self.account['id']).count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.data['count'])

    def test_get_transaction_detail(self):
        """Test retrieving transaction details by ID."""
        url = reverse('transaction-detail', args=[self.transaction['id']])  # URL for transaction detail view
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('vendor item', response.data['description'])

    def test_create_transaction_invalid_data(self):
        """Test creating a transaction with invalid data."""
        invalid_data = {'name': ''}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_transaction(self):
        """Test updating a transaction."""
        url = reverse('transaction-detail', args=[self.transaction['id']])
        updated_data = {
            'date': '2024-02-14',
            'vendor': self.vendor1['url'],
            'description': 'vendor item updated',
            'amount': 30.0,
            'type': 'INC',
            'category': self.category1['url'],
            'account': self.account['url']
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('vendor item updated', response.data['description'])

    def test_update_transaction_owner_to_other_user_account(self):
        """Test updating a transaction."""
        url = reverse('transaction-detail', args=[self.transaction['id']])
        updated_data = {
            'date': '2024-02-14',
            'vendor': self.vendor1['url'],
            'description': 'vendor item updated',
            'amount': 30.0,
            'type': 'INC',
            'category': self.category1['url'],
            'account': 'somehost.com/' + str(self.account2.id) + '/'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_transaction(self):
        """Test deleting a transaction."""
        url = reverse('transaction-detail', args=[self.transaction['id']])
        expected = Transaction.objects.count() - 1
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(expected, Transaction.objects.count())

    def test_get_transaction_unauthorized(self):
        """Test unauthorized access."""
        # Create a new transaction but don't authenticate
        new_transaction_data = {
            'name': 'new-transaction'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_transaction_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, unauthorized_response.status_code)
