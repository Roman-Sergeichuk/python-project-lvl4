from django.contrib import admin

from tasks.models import Tag, Task, TaskStatus

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(Tag)

