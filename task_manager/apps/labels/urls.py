from django.urls import path

from task_manager.apps.labels.views import (
    LabelCreateView,
    LabelDeleteView,
    LabelIndexView,
    LabelUpdateView,
)

urlpatterns = [
    path("", LabelIndexView.as_view(), name="labels_index"),
    path("create/", LabelCreateView.as_view(), name="labels_create"),
    path("<int:pk>/update/", LabelUpdateView.as_view(), name="labels_update"),
    path(
        "<int:pk>/delete/", LabelDeleteView.as_view(), name="labels_delete"
    ),
]
