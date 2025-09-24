from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Label, Status, Task

User = get_user_model()


class LabelsCrudTests(TestCase):
    def setUp(self):
        self.passwd = "s3cret-Pass123"
        self.user = User.objects.create_user(username="john", password=self.passwd)
        self.status = Status.objects.create(name="new")

    def login(self):
        self.client.post(reverse("login"), {"username": "john", "password": self.passwd})

    def test_list_requires_login(self):
        r = self.client.get(reverse("labels_list"))
        self.assertEqual(r.status_code, 302)
        self.login()
        r = self.client.get(reverse("labels_list"))
        self.assertEqual(r.status_code, 200)

    def test_form_field_names(self):
        self.login()
        r = self.client.get(reverse("labels_create"))
        self.assertContains(r, 'name="name"')
        self.assertContains(r, 'id="id_name"')

    def test_create_update_delete(self):
        self.login()
        r = self.client.post(reverse("labels_create"), {"name": "bug"}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Label.objects.filter(name="bug").exists())
        self.assertContains(r, "Label created successfully")
        label = Label.objects.get(name="bug")
        r = self.client.post(
            reverse("labels_update", args=[label.pk]), {"name": "feature"}, follow=True
        )
        self.assertEqual(r.status_code, 200)
        label.refresh_from_db()
        self.assertEqual(label.name, "feature")
        self.assertContains(r, "Label updated successfully")
        r = self.client.post(reverse("labels_delete", args=[label.pk]), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())
        self.assertContains(r, "Label deleted successfully")

    def test_delete_forbidden_if_in_use(self):
        self.login()
        label = Label.objects.create(name="in-use")
        task = Task.objects.create(name="t1", description="", status=self.status, author=self.user)
        task.labels.add(label)
        r = self.client.post(reverse("labels_delete", args=[label.pk]), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())
        self.assertContains(r, "Cannot delete label because it is in use")
