from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
