from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Label, Status, Task

User = get_user_model()


class TasksFilterTests(TestCase):
    def setUp(self):
        self.passwd = "s3cret-Pass123"
        self.author = User.objects.create_user(username="john", password=self.passwd)
        self.other = User.objects.create_user(username="mary", password=self.passwd)
        self.exec1 = User.objects.create_user(username="kate", password=self.passwd)
        self.s_new = Status.objects.create(name="new")
        self.s_work = Status.objects.create(name="work")
        self.l_bug = Label.objects.create(name="bug")
        self.l_feature = Label.objects.create(name="feature")
        self.t1 = Task.objects.create(
            name="t1", description="", status=self.s_new, author=self.author, executor=self.other
        )
        self.t1.labels.add(self.l_bug)
        self.t2 = Task.objects.create(
            name="t2", description="", status=self.s_work, author=self.other, executor=self.exec1
        )
        self.t3 = Task.objects.create(
            name="t3", description="", status=self.s_work, author=self.author
        )
        self.t3.labels.add(self.l_feature)

    def login(self, u="john"):
        self.client.post(reverse("login"), {"username": u, "password": self.passwd})

    def test_filter_form_field_names(self):
        self.login()
        r = self.client.get(reverse("tasks_list"))
        self.assertContains(r, 'name="status"')
        self.assertContains(r, 'id="id_status"')
        self.assertContains(r, 'name="executor"')
        self.assertContains(r, 'name="label"')
        self.assertContains(r, 'name="self_tasks"')

    def test_filter_by_status(self):
        self.login()
        r = self.client.get(reverse("tasks_list"), {"status": self.s_work.pk})
        self.assertContains(r, "t2")
        self.assertContains(r, "t3")
        self.assertNotContains(r, "t1")

    def test_filter_by_executor(self):
        self.login()
        r = self.client.get(reverse("tasks_list"), {"executor": self.other.pk})
        self.assertContains(r, "t1")
        self.assertNotContains(r, "t2")
        self.assertNotContains(r, "t3")

    def test_filter_by_label(self):
        self.login()
        r = self.client.get(reverse("tasks_list"), {"label": self.l_bug.pk})
        self.assertContains(r, "t1")
        self.assertNotContains(r, "t2")
        self.assertNotContains(r, "t3")

    def test_filter_self_tasks(self):
        self.login("john")
        r = self.client.get(reverse("tasks_list"), {"self_tasks": "on"})
        self.assertContains(r, "t1")
        self.assertContains(r, "t3")
        self.assertNotContains(r, "t2")
