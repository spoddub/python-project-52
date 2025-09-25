from django.contrib import messages
from django.contrib.auth.middleware import LoginRequiredMiddleware
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware

from task_manager.apps.core import text_constants


class LoginRequiredWithMessageMiddleware(LoginRequiredMiddleware):
    redirect_field_name = None

    def handle_no_permission(self, request, view_func):
        messages.error(request, text_constants.LOGIN_REQUIRED)
        return super().handle_no_permission(request, view_func)


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):

    def get_payload_data(self, request, exc):
        payload_data = {}

        if not request.user.is_anonymous:
            payload_data = {
                "person": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                },
            }

        return payload_data
