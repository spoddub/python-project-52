from django.contrib.auth import get_user_model
from django.db import models

from task_manager.apps.labels.models import Label
from task_manager.apps.statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.RESTRICT, related_name="tasks_with_status"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="tasks_to_execute",
    )
    author = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="tasks_created"
    )
    labels = models.ManyToManyField(
        Label,
        through="TasksLabels",
        related_name="tasks_with_labels",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class TasksLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.RESTRICT)
