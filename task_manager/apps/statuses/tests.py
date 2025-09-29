from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.apps.core import text_constants
from task_manager.apps.statuses.models import Status


class StatusesTest(TestCase):
    fixtures = ["statuses.json", "users.json"]
    expected_statuses_count = 3
    test_status_id = 2
    testuser_username = "user4"
    testuser_password = "123"
    login_url = reverse("login")
    statuses_index_url = reverse("statuses_index")
    statuses_create_url = reverse("statuses_create")
    statuses_update_url = reverse(
        "statuses_update", kwargs={"pk": test_status_id}
    )
    statuses_delete_url = reverse(
        "statuses_delete", kwargs={"pk": test_status_id}
    )

    def setUp(self):
        user = get_user_model()
        user.objects.create_user(
            username=self.testuser_username,
            password=self.testuser_password,
        )
        self.client.login(
            username=self.testuser_username,
            password=self.testuser_password,
        )

    def test_statuses_index(self):
        response = self.client.get(self.statuses_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("statuses", response.context)
        actual_count = len(response.context["statuses"])
        self.assertEqual(actual_count, self.expected_statuses_count)

    def test_statuses_create(self):
        response = self.client.post(
            self.statuses_create_url,
            data={"name": "Testing"},
            follow=True,
        )
        self.assertRedirects(response, self.statuses_index_url)
        self.assertContains(response, "Testing")
        self.assertContains(response, text_constants.STATUS_CREATED)
        actual_count = len(response.context["statuses"])
        self.assertEqual(actual_count, self.expected_statuses_count + 1)

    def test_statuses_update(self):
        response = self.client.post(
            self.statuses_update_url,
            data={"name": "In review"},
            follow=True,
        )
        self.assertRedirects(response, self.statuses_index_url)
        self.assertContains(response, text_constants.STATUS_UPDATED)
        self.assertContains(response, "In review")
        actual_count = len(response.context["statuses"])
        self.assertEqual(actual_count, self.expected_statuses_count)

    def test_statuses_delete(self):
        status = Status.objects.get(id=self.test_status_id)
        response = self.client.get(self.statuses_delete_url, follow=True)
        delete_confirm_message = text_constants.DELETE_CONFIRM % {
            "name": status.name
        }
        self.assertContains(response, delete_confirm_message)
        response = self.client.post(self.statuses_delete_url, follow=True)
        self.assertRedirects(response, self.statuses_index_url)
        self.assertContains(response, text_constants.STATUS_DELETED)
        actual_count = len(response.context["statuses"])
        self.assertEqual(actual_count, self.expected_statuses_count - 1)


class UnAuthenticatedStatusesTest(TestCase):
    login_url = reverse("login")
    urls = [
        (reverse("statuses_index"), login_url),
        (reverse("statuses_create"), login_url),
        (reverse("statuses_update", kwargs={"pk": 1}), login_url),
        (reverse("statuses_delete", kwargs={"pk": 1}), login_url),
    ]

    def test_statuses_login(self):
        for url, login_url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, f"{login_url}?next={url}")
                self.assertContains(response, text_constants.LOGIN_REQUIRED)
