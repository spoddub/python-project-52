from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Status, Task

User = get_user_model()


class TasksCrudTests(TestCase):
    def setUp(self):
        self.passwd = "s3cret-Pass123"
        self.author = User.objects.create_user(username="john", password=self.passwd)
        self.other = User.objects.create_user(username="mary", password=self.passwd)
        self.status = Status.objects.create(name="new")

    def login_as(self, username):
        self.client.post(reverse("login"), {"username": username, "password": self.passwd})

    def test_list_requires_login(self):
        r = self.client.get(reverse("tasks_list"))
        self.assertEqual(r.status_code, 302)
        self.login_as("john")
        r = self.client.get(reverse("tasks_list"))
        self.assertEqual(r.status_code, 200)

    def test_detail_requires_login(self):
        t = Task.objects.create(name="t1", description="", status=self.status, author=self.author)
        r = self.client.get(reverse("tasks_detail", args=[t.pk]))
        self.assertEqual(r.status_code, 302)
        self.login_as("john")
        r = self.client.get(reverse("tasks_detail", args=[t.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Task:")

    def test_create_sets_author_and_redirects(self):
        self.login_as("john")
        data = {
            "name": "task A",
            "description": "desc",
            "status": self.status.pk,
            "executor": self.other.pk,
        }
        r = self.client.post(reverse("tasks_create"), data, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Task.objects.filter(name="task A").exists())
        t = Task.objects.get(name="task A")
        self.assertEqual(t.author, self.author)
        self.assertEqual(t.executor, self.other)

    def test_update_ok_for_any_logged_user(self):
        t = Task.objects.create(name="t2", description="", status=self.status, author=self.author)
        self.login_as("mary")
        r = self.client.post(
            reverse("tasks_update", args=[t.pk]),
            {"name": "t2x", "description": "upd", "status": self.status.pk, "executor": ""},
            follow=True,
        )
        self.assertEqual(r.status_code, 200)
        t.refresh_from_db()
        self.assertEqual(t.name, "t2x")

    def test_delete_only_author(self):
        t = Task.objects.create(name="t3", description="", status=self.status, author=self.author)
        self.login_as("mary")
        r = self.client.post(reverse("tasks_delete", args=[t.pk]), follow=True)
        self.assertRedirects(r, reverse("tasks_list"))
        self.assertTrue(Task.objects.filter(pk=t.pk).exists())
        self.login_as("john")
        r = self.client.post(reverse("tasks_delete", args=[t.pk]), follow=True)
        self.assertRedirects(r, reverse("tasks_list"))
        self.assertFalse(Task.objects.filter(pk=t.pk).exists())

    def test_user_cannot_be_deleted_if_has_tasks(self):
        Task.objects.create(name="t4", description="", status=self.status, author=self.author)
        self.login_as("john")
        r = self.client.post(reverse("users_delete", args=[self.author.pk]), follow=True)
        self.assertRedirects(r, reverse("users_list"))
        self.assertTrue(User.objects.filter(pk=self.author.pk).exists())
