from django import forms

from tasks.models import Tag, Task, TaskStatus


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'assigned_to', 'tags')
        widgets = {
            'tags': forms.SelectMultiple(),
        }


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ('name',)
        # fields = ('name', 'description', 'status', 'assigned_to', 'tags')
        # widgets = {
        #     'cold': forms.NumberInput(attrs={'style': 'width:100px'}),
        #     'hot': forms.NumberInput(attrs={'style': 'width:100px'})
        # }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
