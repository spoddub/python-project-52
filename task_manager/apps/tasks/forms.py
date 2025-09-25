import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.apps.labels.models import Label
from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task
from task_manager.apps.users.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]

        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }


class TaskFilterForm(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label=_("Status"))

    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label=_("Executor"))

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), label=_("Label"), field_name="labels"
    )

    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method="filter_self_tasks",
        label=_("Own tasks only"),
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
