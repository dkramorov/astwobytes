from django.test import TestCase
from django.urls import reverse

class LoginTests(TestCase):

    auth_url = reverse('login:login_view', args=['auth'])
    admin_url = reverse('login:login_view', args=['admin'])
    auth_logout_url = reverse('login:logout_view', args=['auth'])
    admin_logout_url = reverse('login:logout_view', args=['admin'])

    def test_login_page(self):
        r = self.client.get(self.auth_url)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.admin_url)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.auth_logout_url)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.admin_logout_url)
        self.assertEqual(r.status_code, 200)
