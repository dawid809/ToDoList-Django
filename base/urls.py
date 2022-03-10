from django.urls import path
from .views import ActionCreate, ActionDelete, ActionList, ActionUpdate, TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLogin, RegisterPage , TwoModels
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path('', TaskList.as_view(), name='task-list'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    #(r'^task-update/?P<int:pk>[\d]+)/$
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

    path('task-update/<int:pk>/action-create/', ActionCreate.as_view(), name='action-create'),

    path('action-list/<int:task_pk>/action-update/<int:pk>/', ActionUpdate.as_view(), name='action-update'),
    #path('action-list/', ActionList.as_view(), name='action-list'),
    path('action-list/<int:pk>/', ActionList.as_view(), name='action-list'),
    #path('action-create/', ActionCreate.as_view(), name='action-create'),
    path('action-delete/<int:pk>/', ActionDelete.as_view(), name='action-delete'),
    path('two-models/', TwoModels.as_view(), name='two-models'),

    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
]