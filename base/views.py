from turtle import title
from django import forms
from django.forms.widgets import PasswordInput, TextInput

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy

from .models import Action, Task
# Create your views here.

class ActionList(LoginRequiredMixin,  ListView):
    model = Action
    context_object_name = 'actions'

class ActionCreate(LoginRequiredMixin, CreateView):
    model = Action
    fields =  '__all__'
    success_url = reverse_lazy('task-list')
   # template_name_suffix = 'action_create_form'
    template_name_suffix = 'task_update_form'

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    # paginate_by = 5
    # template_name = 'base/tasks.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search-input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields =  ['title', 'complete']
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =  ['title', 'complete']
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_update_form'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_delete_form'

class CustomLogin(LoginView):
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('task-list')

class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterPage, self).get(*args, **kwargs)