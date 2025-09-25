"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("admin/", admin.site.urls),
    path("login/", views.SignInView.as_view(), name="login"),
    path("logout/", views.LogoutPostOnlyView.as_view(), name="logout"),
    path("users/", views.UsersListView.as_view(), name="users_list"),
    path("users/create/", views.UserCreateView.as_view(), name="users_create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="users_update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="users_delete"),
    path("statuses/", views.StatusListView.as_view(), name="statuses_list"),
    path("statuses/create/", views.StatusCreateView.as_view(), name="statuses_create"),
    path("statuses/<int:pk>/update/", views.StatusUpdateView.as_view(), name="statuses_update"),
    path("statuses/<int:pk>/delete/", views.StatusDeleteView.as_view(), name="statuses_delete"),
    path("tasks/", views.TasksListView.as_view(), name="tasks_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="tasks_create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="tasks_detail"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="tasks_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="tasks_delete"),
    path("labels/", views.LabelsListView.as_view(), name="labels_list"),
    path("labels/create/", views.LabelCreateView.as_view(), name="labels_create"),
    path("labels/<int:pk>/update/", views.LabelUpdateView.as_view(), name="labels_update"),
    path("labels/<int:pk>/delete/", views.LabelDeleteView.as_view(), name="labels_delete"),
]

if settings.DEBUG:
    urlpatterns += [
        path("rollbar-test/", views.rollbar_test_view, name="rollbar_test"),
    ]
