from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.apps.core import text_constants


# Create your tests here.
class AutehicationTest(TestCase):
    fixtures = ["users.json"]

    testuser_username = "user4"
    testuser_password = "123"  # NOSONAR

    main_url = reverse("main")
    login_url = reverse("login")
    logout_url = reverse("logout")

    def setUp(self):
        user = get_user_model()
        user.objects.create_user(
            username=self.testuser_username, password=self.testuser_password
        )

    def test_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            self.login_url,
            data={
                "username": self.testuser_username,
                "password": self.testuser_password,
            },
            follow=True,
        )
        self.assertRedirects(response, self.main_url)
        self.assertContains(response, text_constants.LOGIN_SUCCESS)

    def test_logout(self):
        self.client.login(
            username=self.testuser_username, password=self.testuser_password
        )
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.main_url)
        self.assertContains(response, text_constants.LOGOUT_SUCCESS)
