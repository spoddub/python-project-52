from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager.apps.core import text_constants


class UserPassesTestWithMessageMixin(UserPassesTestMixin):
    permission_denied_message = "You don't have permission to do this"
    redirect_url = "main"

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.error(request, self.permission_denied_message)
            return redirect(reverse_lazy(self.redirect_url))
        return super().dispatch(request, *args, **kwargs)


class UserIsProfileOwnerMixin(UserPassesTestWithMessageMixin):
    permission_denied_message = text_constants.USER_PERMISSION_DENIED
    redirect_url = "users_index"

    def test_func(self):
        return self.request.user.id == self.get_object().id


class UserIsTaskAuthorMixin(UserPassesTestWithMessageMixin):
    permission_denied_message = text_constants.TASK_PERMISSION_DENIED
    redirect_url = "tasks_index"

    def test_func(self):
        return self.request.user.id == self.get_object().author_id


class RedirectOnRestrictedDeleteMixin:
    restict_message = "You can't delete this"
    redirect_url = "main"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except RestrictedError:
            messages.error(self.request, self.restict_message)
            return redirect(reverse_lazy(self.redirect_url))


class RestrictStatusDeleteMixin(RedirectOnRestrictedDeleteMixin):
    restict_message = text_constants.STATUS_RESTRICT_DELETE
    redirect_url = "statuses_index"


class RestrictUserDeleteMixin(RedirectOnRestrictedDeleteMixin):
    restict_message = text_constants.USER_RESTRICT_DELETE
    redirect_url = "users_index"


class RestrictLabelDeleteMixin(RedirectOnRestrictedDeleteMixin):
    restict_message = text_constants.LABEL_RESTRICT_DELETE
    redirect_url = "labels_index"
