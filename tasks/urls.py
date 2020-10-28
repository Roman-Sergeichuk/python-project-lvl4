from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/new/', views.create_task, name='create_task'),
    path('tasks/list/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.update_task, name='update_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/statuses/new/', views.create_status, name='create_status'),
    path('tasks/statuses/list/', views.status_list, name='status_list'),
    path('tasks/statuses/<int:pk>/update/', views.update_status, name='update_status'),
    path('tasks/statuses/<int:pk>/delete/', views.delete_status, name='delete_status'),
    path('tasks/tags/new/', views.create_tag, name='create_tag'),
    path('tasks/tags/list/', views.tag_list, name='tag_list'),
]
