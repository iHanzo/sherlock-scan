from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from fds.custom.log_header import RequestLogMiddleware
from myapp.views import home, register, user_login

class TemplateTests(TestCase):
    def test_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/home.html')
        self.assertContains(response, 'Welcome to the Home Page!')

    def test_register_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/register.html')
        self.assertContains(response, 'Sign Up')

    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/login.html')
        self.assertContains(response, 'Login')

class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.login_url = reverse('login')

    def test_incorrect_authentication(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Invalid username or password.' for message in messages))
        self.assertEqual(response.status_code, 200)

class MiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestLogMiddleware(lambda request: HttpResponse("Just a test response"))

    def test_header_logging(self):
        request = self.factory.post('/some-url', **{'HTTP_CUSTOM_HEADER': 'value'})
        response = self.middleware(request)
        self.assertIsNotNone(response)

    def test_missing_header_handling(self):
        request = self.factory.post('/some-url')
        response = self.middleware(request)
        self.assertIsNotNone(response)
