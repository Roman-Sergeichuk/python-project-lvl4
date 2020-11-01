from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


def index(request):
    return render(request, 'index.html')


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
