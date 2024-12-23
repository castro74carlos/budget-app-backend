from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User
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
        self.assertEqual(response.data['count'], expected)  # Assuming only 1 user in DB

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
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newpassword123'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
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
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password456'
        }
        self.client.force_authenticate(user=None)
        self.client.post(self.url, new_user_data, format='json')
        unauthorized_response = self.client.get(self.url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)