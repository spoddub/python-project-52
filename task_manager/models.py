from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="tasks")
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="authored_tasks", editable=False
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="assigned_tasks", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name
