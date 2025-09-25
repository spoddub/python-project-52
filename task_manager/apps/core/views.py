from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from task_manager.apps.core import text_constants


@method_decorator(login_not_required, name="dispatch")
class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "core/main.html")


@method_decorator(login_not_required, name="dispatch")
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "core/login.html"
    next_page = reverse_lazy("main")
    success_message = text_constants.LOGIN_SUCCESS


@method_decorator(login_not_required, name="dispatch")
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("main")

    def post(self, request, *args, **kwargs):
        messages.info(request, text_constants.LOGOUT_SUCCESS)
        return super().post(request, *args, **kwargs)
