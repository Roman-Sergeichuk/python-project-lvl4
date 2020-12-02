from django.contrib import admin
from tasks.models import Task, TaskStatus, Tag

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(Tag)

