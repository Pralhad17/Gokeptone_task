from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Task

# Register CustomUser model
CustomUser = get_user_model()
admin.site.register(CustomUser)

# Register Task model


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'user')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'due_date')

admin.site.register(Task, TaskAdmin)
