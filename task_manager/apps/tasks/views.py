from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.apps.core import text_constants
from task_manager.apps.core.mixins import UserIsTaskAuthorMixin
from task_manager.apps.tasks.forms import TaskForm
from task_manager.apps.tasks.models import Task


class TaskIndexView(FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = text_constants.TASK_CREATED
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    SuccessMessageMixin,
    UpdateView,
):
    model = Task
    form_class = TaskForm
    success_message = text_constants.TASK_UPDATED
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_index")


class TaskDeleteView(
    UserIsTaskAuthorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    success_message = text_constants.TASK_DELETED
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_index")


class TaskDetailView(
    DetailView,
):
    template_name = "tasks/detail.html"
    model = Task
