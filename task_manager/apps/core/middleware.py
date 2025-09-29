from __future__ import annotations

from typing import Callable

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy

from task_manager.apps.core import text_constants


class LoginRequiredWithMessageMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.login_path = str(reverse_lazy("login"))
        self.signup_path = str(reverse_lazy("users_create"))
        self.users_index_path = str(reverse_lazy("users_index"))
        self.public_paths = {
            "/",
            self.login_path,
            self.signup_path,
            self.users_index_path,
        }

    def __call__(self, request):
        path = request.path
        if path.startswith("/admin/") or (
            settings.STATIC_URL and path.startswith(settings.STATIC_URL)
        ):
            return self.get_response(request)
        if path in self.public_paths:
            return self.get_response(request)
        if not request.user.is_authenticated:
            messages.error(request, text_constants.LOGIN_REQUIRED)
            return redirect_to_login(
                request.get_full_path(),
                login_url=self.login_path,
            )
        return self.get_response(request)


class RollbarNotifierMiddleware:
    _initialized = False

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        if not self._initialized:
            token = settings.ROLLBAR.get("access_token")
            if token:
                try:
                    import rollbar

                    rollbar.init(
                        access_token=token,
                        environment=settings.ROLLBAR.get(
                            "environment",
                            "development" if settings.DEBUG else "production",
                        ),
                        root=str(settings.BASE_DIR),
                        code_version=settings.ROLLBAR.get(
                            "code_version", "1.0"
                        ),
                    )
                except Exception:
                    pass
            self._initialized = True

        try:
            return self.get_response(request)
        except Exception:
            token = settings.ROLLBAR.get("access_token")
            if token:
                try:
                    import rollbar

                    rollbar.report_exc_info()
                except Exception:
                    pass
            raise
