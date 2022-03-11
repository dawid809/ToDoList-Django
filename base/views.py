from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, TimePickerInput

from django.contrib.auth.models import User


from django.urls import reverse_lazy

from .models import Action, Task
# Create your views here.


class ActionList(LoginRequiredMixin, ListView):
    model = Action
    context_object_name = 'actions'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        print(kwargs)
        context['actions'] = context['actions'].filter(task = self.kwargs['task_pk'])
        name = Task.objects.get(id=self.kwargs['task_pk'])
        context['task_name'] = name
        print(context)
        return context


# ModelFormMixin , FormMixin
    # hidden
    # get initial value 
    # id task by pattern(?=123)
class ActionCreate(LoginRequiredMixin, CreateView):
    model = Action
    fields =  ['name', 'started_at', 'ended_at', 'user', 'task']
    template_name_suffix = '_create_form'
  
    def get_success_url(self):
        task_id=self.kwargs['task_pk']
        return reverse_lazy('action-list', kwargs={'task_pk': task_id})

    def get_initial(self):
        initial = super().get_initial()
        print('kwargs: ',self.kwargs)
        initial['task'] = self.kwargs['task_pk']
        initial['user'] = self.request.user
        return initial

    def get_form(self):
        form = super().get_form()
        # form.fields['started_at'].widget = DateTimePickerInput()
        # form.fields['ended_at'].widget = DateTimePickerInput()
        form.fields['started_at'].widget = TimePickerInput()
        form.fields['ended_at'].widget = TimePickerInput()
        form.fields['task'].queryset = Task.objects.filter(id = self.kwargs['task_pk'])
        form.fields['user'].queryset = User.objects.filter(username = self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ActionCreate, self).form_valid(form)
        

class ActionUpdate(LoginRequiredMixin, UpdateView):
    model = Action
    fields =  ['name', 'started_at', 'ended_at']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        task_id=self.kwargs['task_pk']
        return reverse_lazy('action-list', kwargs={'task_pk': task_id})

    def get_initial(self):
        print(self.kwargs)
        print('id_taska = ', self.kwargs['task_pk'])
        return super().get_initial()

    def get_form(self):
        form = super().get_form()
        form.fields['started_at'].widget = TimePickerInput()
        form.fields['ended_at'].widget = TimePickerInput()
        return form


class ActionDelete(LoginRequiredMixin, DeleteView):
    model = Action
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_delete_form'


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

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
    fields =  ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =  ['title', 'description', 'complete']
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
