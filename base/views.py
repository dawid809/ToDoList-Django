
from re import T
from django import forms
from django.forms.widgets import PasswordInput, TextInput

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, TimePickerInput

from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.models import User


from django.urls import reverse_lazy

from base.forms import Form1, Form2

from .models import Action, Task
# Create your views here.

def TwoModels(request):
    action = Action.objects.all()
    task = Task.objects.all()
    return render(request, 'two_models.html', {"Action": action, "Task": task})

# class ActionList(LoginRequiredMixin, ListView):
#     model = Action
#     context_object_name = 'actions'
#     # paginate_by = 5
#     # template_name = 'base/tasks.html'
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context['actions'] = context['actions'].filter(user=self.request.user)
#        # context['count-hours'] = context['actions'].filter()
#         #context['count-hours'] = context['actions'].filter(calctime2=calctime2)
#        # context['actions'] = context['actions'].filter(task)
#        # print('print', context['actions'][1].ended_at) #odwolanie do pola ended dla 1 elementu slownika 
#         return context

class ActionList(LoginRequiredMixin, ListView):
    model = Action
    context_object_name = 'actions'
    # def get_context_data(self, **kwargs):
    #     print(kwargs)
    #     context =  super().get_context_data(**kwargs)
    #     print(kwargs)
    #     context['actions'] = context['actions'].filter(task = self.kwargs['pk'])
    #     name = Task.objects.get(id=self.kwargs['pk'])
    #     context['task_name'] = name
    #     #context['actions'] = context['actions'].filter(user=self.request.user)
    #     return context

# ModelFormMixin , FormMixin
class ActionCreate(LoginRequiredMixin, CreateView):
    model = Action
    fields =  ['name', 'started_at', 'ended_at', 'task', 'user']
    template_name_suffix = '_create_form'

    def get_success_url(self):
        task_id=self.kwargs['pk']
        return reverse_lazy('task-update', kwargs={'pk': task_id})

    def get_initial(self):
        print(self.args)
        #print('id_taska = ', self.kwargs['pk'])
        self.initial['task'] = self.kwargs['pk']
        self.initial['user'] = self.request.user
        
        # hidden
        # get initial value 
        # id task by pattern(?=123)
        return super().get_initial()

    def get_form(self):
        form = super().get_form()
        # form.fields['started_at'].widget = DateTimePickerInput()
        # form.fields['ended_at'].widget = DateTimePickerInput()
        form.fields['started_at'].widget = TimePickerInput()
        form.fields['ended_at'].widget = TimePickerInput()
        form.fields['task'].queryset = Task.objects.filter(id = self.kwargs['pk'])
        form.fields['user'].queryset = User.objects.filter(username = self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ActionCreate, self).form_valid(form)
        

class ActionUpdate(LoginRequiredMixin, UpdateView):
    model = Action
    fields =  ['name', 'started_at', 'ended_at']
    template_name_suffix = '_update_form'

    def get_initial(self):
        print(self.args)
        print('id_taska = ', self.kwargs['pk'])
        return super().get_initial()

    def get_form(self):
        form = super().get_form()
        form.fields['started_at'].widget = TimePickerInput()
        form.fields['ended_at'].widget = TimePickerInput()
        return form

    def get_success_url(self):
        print(self.kwargs)
        task_id=self.kwargs['task_pk']
        action_id=self.kwargs['pk']
        print(task_id, action_id)
        return reverse_lazy('action-list', kwargs={'task_pk': task_id, 'action_pk': action_id})

    def get_queryset(self):
        queryset = super(ActionUpdate, self).get_queryset()
        return queryset.filter(task=self.kwargs['task_pk'])

    # def get_initial(self):
    #     print(self.args)
    #     #print('id_taska = ', self.kwargs['pk'])
    #     self.initial['task'] = self.kwargs['pk']
    #     self.initial['user'] = self.request.user
        
    #     # hidden
    #     # get initial value 
    #     # id task by pattern(?=123)
    #     return super().get_initial()

    # def get_form(self):
    #     form = super().get_form()
    #     # form.fields['started_at'].widget = DateTimePickerInput()
    #     # form.fields['ended_at'].widget = DateTimePickerInput()
    #     form.fields['started_at'].widget = TimePickerInput()
    #     form.fields['ended_at'].widget = TimePickerInput()
    #     form.fields['task'].queryset = Task.objects.filter(id = self.kwargs['pk'])
    #     form.fields['user'].queryset = User.objects.filter(username = self.request.user)
    #     return form

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(ActionUpdate, self).form_valid(form)


class ActionDelete(LoginRequiredMixin, DeleteView):
    model = Action
    success_url = reverse_lazy('task-list')
    template_name_suffix = '_delete_form'

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

    def get_initial(self):
        print(self.args)
        print('id_taska = ', self.kwargs['pk'])
        return super().get_initial()

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


class TwoModels(UpdateView):
    template_name = 'two_models.html'
    success_url = reverse_lazy('/')   
    form_class = Form1
    second_form_class = Form2

    
    def get_context_data(self, **kwargs):
        context = super(TwoModels, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(initial={'some_field': context['model'].some_field})
        if 'form2' not in context:
            context['form2'] = self.second_form_class(initial={'another_field': context['model'].another_field})
        return context

    # def get_object(self):
    #     return get_object_or_404(Task, pk=self.request.session['someval'])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        # get the user instance
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:

            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'

        else:

            # get the secondary form
            form_class = self.second_form_class
            form_name = 'form2'

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

# def index(request):
#     first_form = Form1(request.POST or None)
#     second_form = Form2(request.POST or None)
#     if request.method == 'POST':
#         if 'form1' in request.POST:
#             if first_form.is_valid():
#                 room_code = get_random_string(length=6).upper()
#                 room = Task.objects.create(name=room_code)
#                 room.artists.add(artist)
#                 return render(request, 'room.html', context)
#         elif 'form2' in request.POST:
#             if second_form.is_valid():
#                 artist = join_form.save(commit=False)
#                 room_code = join_form.cleaned_data \
#                     .get('temp_room_code', 'temp code bulunamadi').upper()
#                 room = get_object_or_404(Room, name=room_code)
#                 return render(request, 'room.html', context)
#     context = {'form1': first_form,
#                'form2': second_form}
#     return render(request, 'index.html', context)