from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/task/new/', views.create_task, name='create_task'),
    path('tasks/task/list/', views.task_list, name='task_list'),
    path('tasks/task/<int:pk>/', views.TaskView.as_view(), name='task_detail'),
    path('tasks/task/<int:pk>/update/', views.update_task, name='update_task'),
    path('tasks/task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/status/new/', views.create_status, name='create_status'),
    path('tasks/tag/new/', views.create_tag, name='create_tag'),

]
