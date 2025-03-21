from todo.models import Task
from django.contrib import admin

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "due_date", "is_done")
    list_editable = ("due_date", "is_done")
    sortable_by = ("due_date", "is_done", "title")

admin.site.register(Task, TaskAdmin)
