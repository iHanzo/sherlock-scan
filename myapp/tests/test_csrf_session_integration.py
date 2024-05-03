from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class CSRFSessionIntegrationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_csrf_and_session_integration(self):
        # Get the login page, which should have a CSRF token
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

        # Post credentials to login page
        form_data = {
            'username': 'testuser',
            'password': '12345',
            'csrfmiddlewaretoken': response.context['csrf_token']
        }
        post_response = self.client.post(reverse('login'), data=form_data, follow=True)
        
        # Check if the post is successful and session is maintained
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)
        # Check redirection to the home page
        self.assertRedirects(post_response, reverse('home'))
        # Check the content of the home page to confirm login success
        self.assertContains(post_response, 'Welcome to the Home Page!')
