from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from tasks.filters import TaskFilter
from tasks.models import Tag, Task, TaskStatus

NEW = 'Новая'
COMPLETED = 'Завершена'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'assigned_to', 'tags']
    template_name = 'create_task.html'

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

    def get_initial(self, *args, **kwargs):
        initial = super(TaskCreate, self).get_initial(**kwargs)
        initial['creator'] = self.request.user
        initial['status'] = get_object_or_404(TaskStatus, name=NEW)
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'update_task.html'
    success_url = reverse_lazy('task_list')


class TaskDetail(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_detail.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

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
        return Task.objects.filter(assigned_to=self.request.user).exclude(status__name=COMPLETED)  # noqa: E501


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TaskStatusCreate(LoginRequiredMixin, CreateView):
    model = TaskStatus
    fields = '__all__'
    template_name = 'create_status.html'
    success_url = reverse_lazy('status_list')


class TaskStatusList(LoginRequiredMixin, generic.ListView):
    model = TaskStatus
    template_name = 'status_list.html'
    context_object_name = 'statuses'


class TaskStatusDetail(LoginRequiredMixin, generic.DetailView):
    model = TaskStatus
    template_name = "status_detail.html"
    context_object_name = 'status'


class TaskStatusUpdate(LoginRequiredMixin, UpdateView):
    model = TaskStatus
    fields = '__all__'
    success_url = reverse_lazy('status_list')
    template_name = 'update_status.html'


class TaskStatusDelete(LoginRequiredMixin, DeleteView):
    model = TaskStatus
    success_url = reverse_lazy('status_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TagCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('tag_list')
    template_name = 'create_tag.html'
    error_message = 'Такой тег уже существует'

    def form_invalid(self, form):
        # messages.error(self.request, self.error_message)
        return super().form_invalid(form)



class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('tag_list')
    template_name = 'update_tag.html'


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TagList(LoginRequiredMixin, generic.ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'


class TagDetail(LoginRequiredMixin, generic.DetailView):
    model = Tag
    template_name = "tag_detail.html"
