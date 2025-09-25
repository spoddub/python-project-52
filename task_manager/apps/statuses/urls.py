from django.urls import path

from task_manager.apps.statuses.views import (
    StatusCreateView,
    StatusDeleteView,
    StatusIndexView,
    StatusUpdateView,
)

urlpatterns = [
    path("", StatusIndexView.as_view(), name="statuses_index"),
    path("create/", StatusCreateView.as_view(), name="statuses_create"),
    path(
        "<int:pk>/update/", StatusUpdateView.as_view(), name="statuses_update"
    ),
    path(
        "<int:pk>/delete/", StatusDeleteView.as_view(), name="statuses_delete"
    ),
]
