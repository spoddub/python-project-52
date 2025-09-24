import django_filters
from django import forms
from django.contrib.auth import get_user_model

from .models import Label, Status, Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Status",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Executor",
    )

    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label="Label",
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        widget=forms.CheckboxInput(),
        label="Only my tasks",
    )

    def filter_self_tasks(self, qs, name, value):
        if value:
            return qs.filter(author=self.request.user)
        return qs

    class Meta:
        model = Task
        fields = ("status", "executor", "label", "self_tasks")
