from asyncio import tasks
from audioop import reverse
from datetime import datetime, timezone
from pydoc import resolve
from turtle import title
from django.test import SimpleTestCase, TestCase, Client

from base.views import RegisterPage, TaskCreate, TaskDelete, TaskList, TaskUpdate, CustomLogin
from django.contrib.auth.views import LogoutView
from .models import Task
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from django.db.models.functions import Upper
# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_todo_list_url_resolves(self):
        url = reverse('task-list')
        self.assertEquals(resolve(url).func.view_class, TaskList)

    def test_todo_task_create_resolves(self):
        url = reverse('task-create')
        self.assertEquals(resolve(url).func.view_class, TaskCreate)

    def test_todo_task_update_resolver(self):
        url = reverse('task-update', args=[1])
        self.assertEquals(resolve(url).func.view_class, TaskUpdate)

    def test_todo_task_delete_resolver(self):
        url = reverse('task-delete', args=[2])
        print(url)
        self.assertEquals(resolve(url).func.view_class, TaskDelete)

    def test_todo_login_resolver(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, CustomLogin)

    def test_todo_logout_resolver(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_todo_register_resolver(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterPage)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="dawid123", password="Dawid123!")

    def test_task_list_GET_with_logged_user(self):
        self.client.login(username="dawid123", password="Dawid123!")
        response = self.client.get(reverse('task-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/task_list.html')
    
    
    def test_task_list_GET_without_logged_user(self):
        response = self.client.get(reverse('task-list'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/')

    def test_add_task(self):
        self.client.login(username="dawid123", password="Dawid123!")
        task = Task.objects.create(title="Test title")
        response = self.client.post(reverse('task-create'), {'title': "Test title"})

        self.assertEqual(task.title, "Test title")

    def test_login_view_with_wrong_data(self):
        # self.user = User.objects.create_user(username='*123', password='password')
        login = self.client.login(username="dawid12", password="Dawid123!")
        self.assertEquals(login, False)

class TestModels(TestCase):
    # def setUpData(cls):
    def setUp(self):
        Task.objects.create(user=User.objects.create(username="dawid123", password="Dawid123!"),
         title="Task title 1", description="Task description 11111")

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)
    
    def test_title_value(self):
        tdate = Task.objects.get(id=1).created
        print(tdate)
        task_title = Task.objects.get(id=1).title
        print('title', task_title)
        title = "Task title 1"
        self.assertEqual(task_title, title)

    def test_str_method(self):
        task = Task.objects.get(id=1)
        self.assertEqual(str(task), task.title)
    
    def test_task_ordering(self):
        task = Task.objects.get(id=1)
        ordering = task._meta.ordering
        self.assertEqual(ordering[0], 'complete')
        self.assertEqual(ordering[1], Upper('title'))

    def test_task_complete_default_boolean_value(self):
        task = Task.objects.get(id=1)
        complete = task.complete
        self.assertFalse(complete)

    # # utc zone and utc+1
    # def test_task_created_data(self):
    #     task = Task.objects.get(id=1)
    #     task_date = task.created
    #     date_now = datetime.now()
    #     print(date_now)
    #     self.assertEqual(task_date, date_now)

    """Test Model Label Name"""
    
    def test_user_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
    
    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_complete_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('complete').verbose_name
        self.assertEqual(field_label, 'complete')

    def test_created_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'created')


