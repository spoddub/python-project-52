from django.contrib.auth.decorators import login_not_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.apps.core import text_constants
from task_manager.apps.core.mixins import (
    RestrictUserDeleteMixin,
    UserIsProfileOwnerMixin,
)
from task_manager.apps.users.forms import UserCreateForm, UserUpdateForm
from task_manager.apps.users.models import User


@method_decorator(login_not_required, name="dispatch")
class UserIndexView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


@method_decorator(login_not_required, name="dispatch")
class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    success_message = text_constants.USER_CREATED
    template_name = "users/create.html"
    success_url = reverse_lazy("login")


class UserUpdateView(
    UserIsProfileOwnerMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    form_class = UserUpdateForm
    success_message = text_constants.USER_UPDATED
    template_name = "users/update.html"
    success_url = reverse_lazy("users_index")


class UserDeleteView(
    UserIsProfileOwnerMixin,
    RestrictUserDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    success_message = text_constants.USER_DELETED
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_index")
