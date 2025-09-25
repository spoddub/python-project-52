from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.apps.core import text_constants
from task_manager.apps.core.mixins import RestrictStatusDeleteMixin
from task_manager.apps.statuses.forms import StatusForm
from task_manager.apps.statuses.models import Status


class StatusIndexView(ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    success_message = text_constants.STATUS_CREATED
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_index")


class StatusUpdateView(
    SuccessMessageMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    success_message = text_constants.STATUS_UPDATED
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_index")


class StatusDeleteView(
    RestrictStatusDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Status
    success_message = text_constants.STATUS_DELETED
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_index")
