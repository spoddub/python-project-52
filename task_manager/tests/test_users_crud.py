from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UsersCrudTests(TestCase):
    def setUp(self):
        self.password = "s3cret-pass"
        self.u1 = User.objects.create_user(username="john", password=self.password)
        self.u2 = User.objects.create_user(username="mary", password=self.password)

    def test_list_is_public(self):
        resp = self.client.get(reverse("users_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Users")

    def test_register_redirects_to_login(self):
        url = reverse("users_create")
        data = {
            "username": "newbie",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        resp = self.client.post(url, data, follow=False)
        self.assertRedirects(resp, reverse("login"))

    def test_login_redirects_to_home(self):
        url = reverse("login")
        data = {"username": "john", "password": self.password}
        resp = self.client.post(url, data, follow=False)
        self.assertRedirects(resp, reverse("home"))

    def test_update_self_ok_redirects_to_list(self):
        self.client.login(username="john", password=self.password)
        url = reverse("users_update", args=[self.u1.pk])
        resp = self.client.post(url, {"username": "john"}, follow=False)
        self.assertRedirects(resp, reverse("users_list"))
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.username, "john")

    def test_update_other_forbidden_redirects_to_list(self):
        self.client.login(username="john", password=self.password)
        url = reverse("users_update", args=[self.u2.pk])
        resp = self.client.post(url, {"username": "mary"}, follow=False)
        self.assertRedirects(resp, reverse("users_list"))
        self.u2.refresh_from_db()
        self.assertEqual(self.u2.username, "mary")

    def test_delete_self_ok_redirects_to_list(self):
        self.client.login(username="john", password=self.password)
        url = reverse("users_delete", args=[self.u1.pk])
        resp = self.client.post(url, follow=False)
        self.assertRedirects(resp, reverse("users_list"))
        self.assertFalse(User.objects.filter(pk=self.u1.pk).exists())

    def test_delete_other_forbidden_redirects_to_list(self):
        self.client.login(username="john", password=self.password)
        url = reverse("users_delete", args=[self.u2.pk])
        resp = self.client.post(url, follow=False)
        self.assertRedirects(resp, reverse("users_list"))
        self.assertTrue(User.objects.filter(pk=self.u2.pk).exists())

    def test_logout_is_post_only(self):
        resp = self.client.get(reverse("logout"), follow=False)
        self.assertEqual(resp.status_code, 405)
