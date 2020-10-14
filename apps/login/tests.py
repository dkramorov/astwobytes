from django.test import TestCase
from django.urls import reverse

class LoginTests(TestCase):
    """Тестирование ссылок авторизации и деавторизации из urls.py
    re_path(r'^admin/', include('apps.login.urls')),
    path('auth/', lambda request: redirect('/admin/', permanent=False)),
    """

    auth_url = reverse('login:login_view')
    admin_url = reverse('login:login_view')
    auth_logout_url = reverse('login:logout_view')
    admin_logout_url = reverse('login:logout_view')

    def test_login_page(self):
        r = self.client.get(self.auth_url)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.admin_url)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.auth_logout_url)
        self.assertEqual(r.status_code, 302)
        r = self.client.get(self.admin_logout_url)
        self.assertEqual(r.status_code, 302)
