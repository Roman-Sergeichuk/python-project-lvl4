from django.urls import path
from . import views


urlpatterns = [
    # path('new/', views.create_task, name='create_task'),
    path('', views.task_list, name='task_list'),
    path('new/', views.TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    # path('update/<int:pk>/', views.update_task, name='update_task'),
    path('<int:pk>/update', views.TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete', views.delete_task, name='delete_task'),
    # path('statuses/new/', views.create_status, name='create_status'),
    path('statuses/new/', views.TaskStatusCreate.as_view(), name='create_status'),
    path('statuses/', views.status_list, name='status_list'),
    path('statuses/<int:pk>', views.status_detail, name='status_detail'),
    # path('statuses/<int:pk>/update/', views.update_status, name='update_status'),
    path('statuses/<int:pk>/update', views.TaskStatusUpdate.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete', views.delete_status, name='delete_status'),
    # path('tags/new/', views.create_tag, name='create_tag'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/new/', views.TagCreate.as_view(), name='create_tag'),
]
