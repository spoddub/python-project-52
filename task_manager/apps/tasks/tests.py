from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest_parametrize import ParametrizedTestCase, parametrize

from task_manager.apps.core import text_constants
from task_manager.apps.tasks.models import Task


class TasksTest(TestCase):
    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]
    expected_tasks_count = 4
    status_filter_tasks_count = 2
    executor_filter_tasks_count = 2
    own_tasks_filter_tasks_count = 1
    full_filter_tasks_count = 1
    test_task_id = 2
    delete_task_id = 5
    wrong_delete_task_id = 2
    testuser_username = "user4"
    testuser_password = "123"  # NOSONAR
    new_task_data = {
        "name": "New task",
        "description": "New description",
        "status": 1,
        "executor": 1,
    }

    login_url = reverse("login")
    tasks_index_url = reverse("tasks_index")
    tasks_create_url = reverse("tasks_create")
    tasks_update_url = reverse("tasks_update", kwargs={"pk": test_task_id})
    tasks_read_url = reverse("tasks_update", kwargs={"pk": test_task_id})
    tasks_delete_url = reverse("tasks_delete", kwargs={"pk": delete_task_id})
    tasks_with_user_delete_url = reverse("tasks_delete", kwargs={"pk": 1})
    tasks_wrong_delete_url = reverse(
        "tasks_delete", kwargs={"pk": wrong_delete_task_id}
    )
    tasks_filter_status_url = reverse("tasks_index", query={"status": 2})
    tasks_filter_executor_url = reverse("tasks_index", query={"executor": 2})
    tasks_filter_own_tasks_url = reverse(
        "tasks_index", query={"self_tasks": "on"}
    )
    tasks_filter_full_url = reverse(
        "tasks_index", query={"status": 1, "executor": 1, "self_tasks": "on"}
    )
    delete_user_with_task_url = reverse("users_delete", kwargs={"pk": 4})
    delete_status_with_task_url = reverse("statuses_delete", kwargs={"pk": 1})
    delete_label_with_task_url = reverse("labels_delete", kwargs={"pk": 1})

    def setUp(self):
        user = get_user_model()
        user.objects.create_user(
            username=self.testuser_username, password=self.testuser_password
        )
        self.client.login(
            username=self.testuser_username, password=self.testuser_password
        )

    def test_tasks_index(self):
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasks", response.context)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.expected_tasks_count)

    def test_tasks_create(self):
        response = self.client.post(
            self.tasks_create_url,
            data=self.new_task_data,
            follow=True,
        )
        self.assertRedirects(response, self.tasks_index_url)
        self.assertContains(response, text_constants.TASK_CREATED)
        self.assertContains(response, "New task")
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.expected_tasks_count + 1)

    def test_tasks_update(self):
        response = self.client.post(
            self.tasks_update_url,
            data={
                "name": "Updated task name",
                "description": "New description",
                "status": 1,
                "executor": 1,
            },
            follow=True,
        )
        self.assertRedirects(response, self.tasks_index_url)
        self.assertContains(response, text_constants.TASK_UPDATED)
        self.assertContains(response, "Updated task name")
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.expected_tasks_count)

    def test_tasks_delete(self):
        task_to_delete = Task.objects.create(
            name="Task_to_delete", status_id=1, executor_id=1, author_id=4
        )
        response = self.client.get(self.tasks_delete_url, follow=True)
        delete_confirm_message = text_constants.DELETE_CONFIRM % {
            "name": task_to_delete.name
        }
        self.assertContains(response, delete_confirm_message)
        response = self.client.post(self.tasks_delete_url, follow=True)
        self.assertRedirects(response, self.tasks_index_url)
        self.assertContains(response, text_constants.TASK_DELETED)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.expected_tasks_count)

    def test_tasks_wrong_delete(self):
        response = self.client.get(self.tasks_wrong_delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text_constants.TASK_PERMISSION_DENIED)

    def test_tasks_filter_status(self):
        response = self.client.get(self.tasks_filter_status_url)
        self.assertEqual(response.status_code, 200)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.status_filter_tasks_count)

    def test_tasks_filter_executor(self):
        response = self.client.get(self.tasks_filter_executor_url)
        self.assertEqual(response.status_code, 200)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.executor_filter_tasks_count)

    def test_tasks_filter_own_tasks(self):
        self.client.post(
            self.tasks_create_url,
            data=self.new_task_data,
            follow=True,
        )
        response = self.client.get(self.tasks_filter_own_tasks_url)
        self.assertEqual(response.status_code, 200)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.own_tasks_filter_tasks_count)

    def test_tasks_filter_full(self):
        self.client.post(
            self.tasks_create_url,
            data=self.new_task_data,
            follow=True,
        )
        response = self.client.get(self.tasks_filter_full_url)
        self.assertEqual(response.status_code, 200)
        actual_tasks_count = len(response.context["tasks"])
        self.assertEqual(actual_tasks_count, self.full_filter_tasks_count)

    def test_tasks_user_delete_restrict(self):
        self.client.post(
            self.tasks_create_url,
            data=self.new_task_data,
            follow=True,
        )
        response = self.client.post(
            reverse("users_delete", kwargs={"pk": 4}), follow=True
        )
        self.assertContains(response, text_constants.USER_RESTRICT_DELETE)

    def test_tasks__with_status_delete_restrict(self):
        response = self.client.post(
            self.delete_status_with_task_url, follow=True
        )
        self.assertContains(response, text_constants.STATUS_RESTRICT_DELETE)

    def test_tasks__with_label_delete_restrict(self):
        response = self.client.post(
            self.delete_label_with_task_url, follow=True
        )
        self.assertContains(response, text_constants.LABEL_RESTRICT_DELETE)


class UnAuthenticatedTasksTest(ParametrizedTestCase, TestCase):
    login_url = reverse("login")
    urls = [
        (reverse("tasks_index"), login_url),
        (reverse("tasks_create"), login_url),
        (reverse("tasks_update", kwargs={"pk": 1}), login_url),
        (reverse("tasks_delete", kwargs={"pk": 1}), login_url),
    ]

    @parametrize("url,login_url", urls)
    def test_tasks_login(self, url, login_url):
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, login_url)
        self.assertContains(response, text_constants.LOGIN_REQUIRED)
