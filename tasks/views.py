from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from tasks.filters import TaskFilter
from tasks.models import Tag, Task, TaskStatus

NEW = 'Новая'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'
    template_name = 'create_task.html'
    success_url = reverse_lazy('task_list')

    def get_initial(self, *args, **kwargs):
        initial = super(TaskCreate, self).get_initial(**kwargs)
        initial['creator'] = self.request.user
        initial['status'] = get_object_or_404(TaskStatus, name=NEW)
        return initial


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'update_task.html'
    success_url = reverse_lazy('task_list')


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def task_list(request):
    f = TaskFilter(request.GET, queryset=Task.objects.all())
    return render(request, 'task_list.html', {'filter': f})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect(reverse('task_list'))


class TaskStatusCreate(LoginRequiredMixin, CreateView):
    model = TaskStatus
    fields = '__all__'
    template_name = 'create_status.html'
    success_url = reverse_lazy('status_list')


@login_required
def status_list(request):
    statuses = TaskStatus.objects.all()
    return render(request, 'status_list.html', {'statuses': statuses})


@login_required
def status_detail(request, pk):
    status = get_object_or_404(TaskStatus, pk=pk)
    return render(request, 'status_detail.html', {'status': status})


class TaskStatusUpdate(LoginRequiredMixin, UpdateView):
    model = TaskStatus
    fields = '__all__'
    success_url = reverse_lazy('status_list')
    template_name = 'update_status.html'


@login_required
def delete_status(request, pk):
    status = get_object_or_404(TaskStatus, pk=pk)
    status.delete()
    return redirect(reverse('status_list'))


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('tag_list')
    template_name = 'create_tag.html'


@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})
