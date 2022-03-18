from audioop import reverse
from datetime import  time
from pydoc import resolve
from django.test import SimpleTestCase, TestCase, Client

from base.views import ActionCreate, ActionDelete, ActionList, ActionUpdate, RegisterPage, TaskCreate, TaskDelete, TaskDetail, TaskList, TaskUpdate, CustomLogin
from django.contrib.auth.views import LogoutView
from .models import Task, Action
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from django.db.models.functions import Upper

# Create your tests here.

class TestUrls(SimpleTestCase):
    
    def test_todo_task_list_url_resolves(self):
        url = reverse('task-list')
        self.assertEqual(resolve(url).func.view_class, TaskList)

    def test_todo_task_create_resolves(self):
        url = reverse('task-create')
        self.assertEqual(resolve(url).func.view_class, TaskCreate)

    def test_todo_task_update_resolver(self):
        url = reverse('task-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskUpdate)

    def test_todo_task_delete_resolver(self):
        url = reverse('task-delete', args=[2])
        self.assertEqual(resolve(url).func.view_class, TaskDelete)

    def test_todo_task_detail_resolver(self):
        url = reverse('task-detail', args=[2])
        self.assertEqual(resolve(url).func.view_class, TaskDetail)

    def test_todo_action_list_resolver(self):
        url = reverse('action-list', args=[5])
        self.assertEqual(resolve(url).func.view_class, ActionList)

    def test_todo_action_create_resolver(self):
        url = reverse('action-create', args=[3])
        self.assertEqual(resolve(url).func.view_class, ActionCreate)

    def test_todo_action_update_resolver(self):
        url = reverse('action-update', args = [3, 5])
        self.assertEqual(resolve(url).func.view_class, ActionUpdate)

    def test_todo_action_delete_resolver(self):
        url = reverse('action-delete', args=[4, 44])
        self.assertEqual(resolve(url).func.view_class, ActionDelete)

    def test_todo_login_resolver(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLogin)

    def test_todo_logout_resolver(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_todo_register_resolver(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterPage)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="dawid123", password="Dawid123!")

    def test_task_list_GET_with_logged_user(self):
        self.client.login(username="dawid123", password="Dawid123!")
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/task_list.html')
    
    
    def test_task_list_GET_without_logged_user(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/')

    def test_task_add_task(self):
        self.client.login(username="dawid123", password="Dawid123!")
        task = Task.objects.create(user_id = 1, title="Test title", description="test description")

        self.assertEqual(task.user_id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "test description")

    def test_login_view_with_wrong_data(self):
        login = self.client.login(username="dawid12", password="Dawid123!")
        self.assertEqual(login, False)

class TestModels(TestCase):
    def setUp(self):
        user_init = User.objects.create(username="dawid123", password="Dawid123!")
        task_init = Task.objects.create(user=user_init, title="Task title 1", description="Task description 11111")
        t_start = '12:11:00'
        t_end = '13:11:00'
        action_init = Action.objects.create(name="action 1", started_at=t_start, ended_at=t_end,task = task_init)

        print(user_init, task_init, action_init)

    def test_task_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)
    
    def test_task_user_username_value(self):
        user = Task.objects.get(id=1).user.username
        user_username = "dawid123"
        self.assertEqual(user, user_username)

    def test_task_title_value(self):
        task_title = Task.objects.get(id=1).title
        title = "Task title 1"
        self.assertEqual(task_title, title)

    def test_task_description_value(self):
        task_description = Task.objects.get(id=1).description
        description = "Task description 11111"
        self.assertEqual(task_description, description)

    def test_task_complete_default_boolean_value(self):
        task = Task.objects.get(id=1)
        complete = task.complete
        self.assertFalse(complete)

        # # utc zone and utc+1
    # def test_task_created_data_value(self):
    #     task = Task.objects.get(id=1)
    #     task_date = task.created
    #     date_now = datetime.now() - timedelta(hours=1)
    #     print(date_now)
    #     self.assertEqual(task_date, date_now)

    def test_task_str_method(self):
        task = Task.objects.get(id=1)
        self.assertEqual(str(task), task.title)
    
    def test_task_ordering(self):
        task = Task.objects.get(id=1)
        ordering = task._meta.ordering
        self.assertEqual(ordering[0], 'complete')
        self.assertEqual(ordering[1], Upper('title'))

    def test_action_name_max_length(self):
        action = Action.objects.get(id=1)
        max_length = action._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_action_name_value(self):
        action = Action.objects.get(id=1).name
        action_name = 'action 1'
        self.assertEqual(action, action_name)

    def test_action_started_at_value(self):
        action = Action.objects.get(id=1).started_at
        t_start = time(12, 11)
        self.assertEqual(action, t_start)

    def test_action_ended_at_value(self):
        action = Action.objects.get(id=1).ended_at
        t_end = time(13, 11)
        self.assertEqual(action, t_end)

        ## test form time validation
    # def test_action_started_at_greater_than_ended_at_validation_error(self):
    #     #task_init = Task.objects.create(user=user_init, title="Task title 1", description="Task description 11111")
    #     #t_start = time(14, 14)
    #     #t_end = time(13, 11)
    #     action = Action.objects.get(id=1).started_at = time(20,12)
    #     #action = Action.objects.create(user=User.objects.get(username="dawid123"), name="action 1", started_at=t_start, ended_at=t_end,task = task_init)
    #     self.assertFormError(form=ActionForm, field='started_at', errors=ValidationError)

    def test_action_str_method(self):
        action = Action.objects.get(id=1)
        self.assertEqual(str(action), action.name)

    def test_action_ordering(self):
        action = Action.objects.get(id=1)
        ordering = action._meta.ordering
        self.assertEqual(ordering[0], Upper('name'))

    """Test Model Label Name"""
    
    def test_task_user_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_task_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
    
    def test_task_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_task_complete_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('complete').verbose_name
        self.assertEqual(field_label, 'complete')

    def test_task_created_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'created')

    def test_action_name_label(self):
        action = Action.objects.get(id=1)
        field_label = action._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_action_started_at_label(self):
        action = Action.objects.get(id=1)
        field_label = action._meta.get_field('started_at').verbose_name
        self.assertEqual(field_label, 'started at')

    def test_action_ended_at_label(self):
        action = Action.objects.get(id=1)
        field_label = action._meta.get_field('ended_at').verbose_name
        self.assertEqual(field_label, 'ended at')

    def test_action_task_label(self):
        action = Action.objects.get(id=1)
        field_label = action._meta.get_field('task').verbose_name
        self.assertEqual(field_label, 'task')


