from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/task/new/', views.create_task, name='create_task'),
    path('tasks/task/list/', views.task_list, name='task_list'),
    path('tasks/task/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/task/<int:pk>/update/', views.update_task, name='update_task'),
    path('tasks/task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/status/new/', views.create_status, name='create_status'),
    path('tasks/status/list/', views.status_list, name='status_list'),
    path('tasks/status/<int:pk>/update/', views.update_status, name='update_status'),
    path('tasks/status/<int:pk>/delete/', views.delete_status, name='delete_status'),
    path('tasks/tag/new/', views.create_tag, name='create_tag'),
    path('tasks/tag/list/', views.tag_list, name='tag_list'),
]
