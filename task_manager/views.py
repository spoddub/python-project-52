import rollbar
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Label, Status, Task


def index(request):
    return render(request, "index.html")


User = get_user_model()


class UsersListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)


class OnlySelfMixin(UserPassesTestMixin):
    permission_denied_message = "У вас нет прав для изменения другого пользователя."

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.pk == self.request.user.pk

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect("users_list")


class UserUpdateView(LoginRequiredMixin, OnlySelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменён")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, OnlySelfMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Пользователь успешно удалён")
        except ProtectedError:
            messages.error(request, "Невозможно удалить пользователя, потому что он используется")
        return redirect(self.success_url)


class SignInView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class LogoutPostOnlyView(LogoutView):
    http_method_names = ["post"]
    next_page = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().post(request, *args, **kwargs)


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменён")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Статус успешно удалён")
        except ProtectedError:
            messages.error(request, "Невозможно удалить статус, потому что он используется")
        return redirect(self.success_url)


class OnlyAuthorDeleteMixin(UserPassesTestMixin):
    permission_denied_message = "Задачу может удалить только её автор."

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect("tasks_list")


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    paginate_by = 20

    def get_queryset(self):
        return (
            Task.objects.select_related("status", "author", "executor")
            .prefetch_related("labels")
            .all()
        )


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, OnlyAuthorDeleteMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Задача успешно удалена")
        return redirect(self.success_url)


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, "Невозможно удалить метку, потому что она используется")
            return redirect(self.success_url)
        self.object.delete()
        messages.success(request, "Метка успешно удалена")
        return redirect(self.success_url)


def rollbar_test_view(request):
    rollbar.report_message("Rollbar test ping from /rollbar-test/", "info")
    raise RuntimeError("Rollbar test exception")
