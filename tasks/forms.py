from django import forms

from tasks.models import Tag, Task, TaskStatus


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'tags': forms.SelectMultiple(),
            'creator': forms.HiddenInput,
        }


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ('name',)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
