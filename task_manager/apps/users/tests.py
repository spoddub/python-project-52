from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.urls import reverse

from task_manager.apps.core import text_constants


class UnAuthenticatedUsersTest(TestCase):
    fixtures = ["users.json"]
    expected_users_count = 3

    mismatched_passwords_message = UserCreationForm.error_messages[
        "password_mismatch"
    ]

    login_url = reverse("login")
    index_users_url = reverse("users_index")
    create_user_url = reverse("users_create")

    def test_user_index(self):
        response = self.client.get(self.index_users_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)
        actual_users_count = len(response.context["users"])
        self.assertEqual(actual_users_count, self.expected_users_count)

    def test_user_create(self):
        response = self.client.post(
            self.create_user_url,
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john12",
                "password1": "123",  # NOSONAR
                "password2": "123",  # NOSONAR
            },
            follow=True,
        )
        self.assertRedirects(response, self.login_url)
        self.assertContains(response, text_constants.USER_CREATED)

        response = self.client.get(self.index_users_url)
        self.assertContains(response, "John Doe")
        actual_users_count = len(response.context["users"])
        self.assertEqual(actual_users_count, self.expected_users_count + 1)

    def test_user_create_not_matching_passwords(self):
        response = self.client.post(
            self.create_user_url,
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john12",
                "password1": "123",  # NOSONAR
                "password2": "321",  # NOSONAR
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mismatched_passwords_message)


class AuthenticatedUsersTest(TestCase):
    fixtures = ["users.json"]
    testuser_username = "user4"
    testuser_password = "123"  # NOSONAR
    test_user_id = 4
    expected_users_count = 4

    login_url = reverse("login")
    index_users_url = reverse("users_index")
    update_user_url = reverse("users_update", kwargs={"pk": test_user_id})
    update_wrong_user_url = reverse(
        "users_update", kwargs={"pk": test_user_id - 1}
    )
    delete_user_url = reverse("users_delete", kwargs={"pk": test_user_id})
    delete_wrong_user_url = reverse(
        "users_delete", kwargs={"pk": test_user_id - 1}
    )

    def setUp(self):
        user = get_user_model()
        user.objects.create_user(
            username=self.testuser_username, password=self.testuser_password
        )
        self.client.login(
            username=self.testuser_username, password=self.testuser_password
        )

    def test_user_update(self):
        response = self.client.post(
            self.update_user_url,
            data={
                "first_name": "Bob",
                "last_name": "Tompson",
                "username": "bob_18",
                "password1": self.testuser_password,
                "password2": self.testuser_password,
            },
            follow=True,
        )
        self.assertRedirects(response, self.index_users_url)
        self.assertContains(response, text_constants.USER_UPDATED)
        self.assertContains(response, "Bob Tompson")
        actual_users_count = len(response.context["users"])
        self.assertEqual(actual_users_count, self.expected_users_count)

    def test_wrong_user_update(self):
        response = self.client.get(self.update_wrong_user_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text_constants.USER_PERMISSION_DENIED)

    def test_user_delete(self):
        user_model = get_user_model()
        user = user_model.objects.get(id=self.test_user_id)
        response = self.client.get(self.delete_user_url, follow=True)
        delete_confirm_message = text_constants.DELETE_CONFIRM % {
            "name": str(user)
        }
        self.assertContains(response, delete_confirm_message)
        response = self.client.post(self.delete_user_url, follow=True)
        self.assertRedirects(response, self.index_users_url)
        self.assertContains(response, text_constants.USER_DELETED)
        actual_users_count = len(response.context["users"])
        self.assertEqual(actual_users_count, self.expected_users_count - 1)

    def test_wrong_user_delete(self):
        response = self.client.get(self.delete_wrong_user_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text_constants.USER_PERMISSION_DENIED)


class UnAuthenticatedUserssTest(TestCase):
    login_url = reverse("login")
    urls = [
        (reverse("users_update", kwargs={"pk": 1}), login_url),
        (reverse("users_delete", kwargs={"pk": 1}), login_url),
    ]

    def test_users_login(self):
        for url, login_url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, f"{login_url}?next={url}")
                self.assertContains(response, text_constants.LOGIN_REQUIRED)
