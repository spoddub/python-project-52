from django.urls import path

from task_manager.apps.core.views import (
    MainView,
    UserLoginView,
    UserLogoutView,
)

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
