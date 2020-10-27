from django.shortcuts import render,get_object_or_404
from tasks.forms import TaskStatusForm, TaskForm, TagForm
from tasks.models import Task
from django.views import generic
from tasks.filters import TaskFilter


def index(request):
    return render(request, 'index.html')


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            return render(request, 'index.html')
    else:
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})


class TaskView(generic.DetailView):
    model = Task
    template_name = "task_detail.html"


def task_list(request):
    f = TaskFilter(request.GET, queryset=Task.objects.all())
    return render(request, 'task_list.html', {'filter': f})


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'task_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(
            self.request.GET,
            queryset=self.get_queryset(),
        )
        return context

    def get_queryset(self):
        if self.request.GET:
            parameters = self.request.GET
            filters = {}
            for key, value in parameters.items():
                if value:
                    filters[key] = value
            return Task.objects.filter(**filters)
        return Task.objects.all()


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            return render(request, 'index.html')
    else:
        form = TaskForm(instance=task)
        return render(request, 'update_task.html', {'form': form})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    # return redirect(reverse('user_readings_list', kwargs={'pk': user_id}))
    return render(request, 'index.html')


def create_status(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return render(request, 'index.html')
    else:
        form = TaskStatusForm()
        return render(request, 'create_status.html', {'form': form})


def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return render(request, 'index.html')
    else:
        form = TaskStatusForm()
        return render(request, 'create_tag.html', {'form': form})
