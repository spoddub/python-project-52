from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Status

User = get_user_model()


class StatusesCrudTests(TestCase):
    def setUp(self):
        self.password = "s3cret-pass"
        self.user = User.objects.create_user(username="john", password=self.password)

    def login(self):
        self.client.post(reverse("login"), {"username": "john", "password": self.password})

    def test_list_requires_auth(self):
        resp = self.client.get(reverse("statuses_list"))
        self.assertEqual(resp.status_code, 302)  # redirect to login
        self.login()
        resp = self.client.get(reverse("statuses_list"))
        self.assertEqual(resp.status_code, 200)

    def test_create_update_delete(self):
        self.login()
        # create
        resp = self.client.post(reverse("statuses_create"), {"name": "new"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Status.objects.filter(name="new").exists())
        # update
        st = Status.objects.get(name="new")
        resp = self.client.post(
            reverse("statuses_update", args=[st.pk]), {"name": "working"}, follow=True
        )
        self.assertEqual(resp.status_code, 200)
        st.refresh_from_db()
        self.assertEqual(st.name, "working")
        # delete
        resp = self.client.post(reverse("statuses_delete", args=[st.pk]), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Status.objects.filter(pk=st.pk).exists())

    def test_form_field_names(self):
        self.login()
        resp = self.client.get(reverse("statuses_create"))
        self.assertContains(resp, 'name="name"')
        self.assertContains(resp, 'id="id_name"')
