from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.apps.core import text_constants
from task_manager.apps.core.mixins import RestrictLabelDeleteMixin
from task_manager.apps.labels.forms import LabelsForm
from task_manager.apps.labels.models import Label


class LabelIndexView(ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelsForm
    success_message = text_constants.LABEL_CREATED
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_index")


class LabelUpdateView(
    SuccessMessageMixin,
    UpdateView,
):
    model = Label
    form_class = LabelsForm
    success_message = text_constants.LABEL_UPDATED
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_index")


class LabelDeleteView(
    RestrictLabelDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Label
    success_message = text_constants.LABEL_DELETED
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_index")
