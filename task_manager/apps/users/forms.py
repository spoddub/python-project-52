from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from task_manager.apps.users.models import User


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last Name"),
            "username": _("Username"),
        }


class UserUpdateForm(UserCreateForm):

    def clean_username(self):
        """Reject usernames that differ only in case.
            Doesn't include current username"""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.exclude(pk=self.instance.pk)
            .filter(username__iexact=username)
            .exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username
