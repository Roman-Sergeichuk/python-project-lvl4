from django.shortcuts import render, get_object_or_404, redirect
from tasks.forms import TaskStatusForm, TaskForm, TagForm
from tasks.models import Task, TaskStatus, Tag
from tasks.filters import TaskFilter
from django.urls import reverse
from django.contrib.auth.decorators import login_required


NEW = 'Новая'


def index(request):
    return render(request, 'index.html')


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, initial={'status': get_object_or_404(TaskStatus, name=NEW)})
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            return redirect(reverse('task_detail', kwargs={'pk': task.pk}))
    else:
        form = TaskForm(initial={'status': get_object_or_404(TaskStatus, name=NEW)})
        return render(request, 'create_task.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def task_list(request):
    f = TaskFilter(request.GET, queryset=Task.objects.all())
    return render(request, 'task_list.html', {'filter': f})


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            return redirect(reverse('task_detail', kwargs={'pk': task.pk}))
    else:
        form = TaskForm(instance=task)
        return render(request, 'update_task.html', {'form': form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect(reverse('task_list'))


@login_required
def create_status(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            return redirect(reverse('status_list'))
    else:
        form = TaskStatusForm()
        return render(request, 'create_status.html', {'form': form})


@login_required
def status_list(request):
    statuses = TaskStatus.objects.all()
    return render(request, 'status_list.html', {'statuses': statuses})


@login_required
def update_status(request, pk):
    status = get_object_or_404(TaskStatus, pk=pk)
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            return redirect(reverse('status_list'))
    else:
        form = TaskStatusForm(instance=status)
        return render(request, 'update_status.html', {'form': form})


@login_required
def delete_status(request, pk):
    status = get_object_or_404(TaskStatus, pk=pk)
    status.delete()
    return redirect(reverse('status_list'))


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect(reverse('tag_list'))
    else:
        form = TaskStatusForm()
        return render(request, 'create_tag.html', {'form': form})


@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})
