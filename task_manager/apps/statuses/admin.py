from django.contrib import admin

from task_manager.apps.statuses.models import Status

# Register your models here.

admin.site.register(Status)
