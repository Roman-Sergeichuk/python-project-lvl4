import django_filters
from django.shortcuts import get_object_or_404
from tasks.models import NEW

from tasks.models import Task, TaskStatus


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'creator', 'tags', 'assigned_to']

