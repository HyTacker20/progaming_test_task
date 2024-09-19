from django.contrib import admin

from task_management_system.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "priority",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description")
