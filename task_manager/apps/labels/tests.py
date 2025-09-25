from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest_parametrize import ParametrizedTestCase, parametrize

from task_manager.apps.core import text_constants
from task_manager.apps.labels.models import Label


class StatusesTest(TestCase):
    fixtures = ["labels.json", "users.json"]
    expected_labels_count = 3
    test_label_id = 2
    testuser_username = "user4"
    testuser_password = "123"  # NOSONAR

    login_url = reverse("login")
    labels_index_url = reverse("labels_index")
    labels_create_url = reverse("labels_create")
    labels_update_url = reverse("labels_update", kwargs={"pk": test_label_id})
    labels_delete_url = reverse("labels_delete", kwargs={"pk": test_label_id})

    def setUp(self):
        user = get_user_model()
        user.objects.create_user(
            username=self.testuser_username, password=self.testuser_password
        )
        self.client.login(
            username=self.testuser_username, password=self.testuser_password
        )

    def test_labels_index(self):
        response = self.client.get(self.labels_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("labels", response.context)
        actual_labels_count = len(response.context["labels"])
        self.assertEqual(actual_labels_count, self.expected_labels_count)

    def test_labels_create(self):
        response = self.client.post(
            self.labels_create_url,
            data={"name": "Testing"},
            follow=True,
        )
        self.assertRedirects(response, self.labels_index_url)
        self.assertContains(response, "Testing")
        self.assertContains(response, text_constants.LABEL_CREATED)
        actual_labels_count = len(response.context["labels"])
        self.assertEqual(actual_labels_count, self.expected_labels_count + 1)

    def test_labels_update(self):
        response = self.client.post(
            self.labels_update_url,
            data={
                "name": "Bug fixing",
            },
            follow=True,
        )
        self.assertRedirects(response, self.labels_index_url)
        self.assertContains(response, text_constants.LABEL_UPDATED)
        self.assertContains(response, "Bug fixing")
        actual_labels_count = len(response.context["labels"])
        self.assertEqual(actual_labels_count, self.expected_labels_count)

    def test_labels_delete(self):
        label = Label.objects.get(id=self.test_label_id)
        response = self.client.get(self.labels_delete_url, follow=True)
        delete_confirm_message = text_constants.DELETE_CONFIRM % {
            "name": label.name
        }
        self.assertContains(response, delete_confirm_message)
        response = self.client.post(self.labels_delete_url, follow=True)
        self.assertRedirects(response, self.labels_index_url)
        self.assertContains(response, text_constants.LABEL_DELETED)
        actual_labels_count = len(response.context["labels"])
        self.assertEqual(actual_labels_count, self.expected_labels_count - 1)


class UnAuthenticatedLabelsTest(ParametrizedTestCase, TestCase):
    login_url = reverse("login")
    urls = [
        (reverse("labels_index"), login_url),
        (reverse("labels_create"), login_url),
        (reverse("labels_update", kwargs={"pk": 1}), login_url),
        (reverse("labels_delete", kwargs={"pk": 1}), login_url),
    ]

    @parametrize("url,login_url", urls)
    def test_labels_login(self, url, login_url):
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, login_url)
        self.assertContains(response, text_constants.LOGIN_REQUIRED)
