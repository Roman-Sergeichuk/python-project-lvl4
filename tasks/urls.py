from django.urls import path

from . import views

urlpatterns = [
    # path('', views.task_list, name='task_list'),
    path('', views.TaskListView.as_view(), name='task_list'),
    path('new/', views.TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update', views.TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete', views.delete_task, name='delete_task'),
    path('statuses/new/', views.TaskStatusCreate.as_view(), name='create_status'),  # noqa: E501
    path('statuses/', views.status_list, name='status_list'),
    path('statuses/<int:pk>', views.status_detail, name='status_detail'),
    path('statuses/<int:pk>/update', views.TaskStatusUpdate.as_view(), name='update_status'),  # noqa: E501
    path('statuses/<int:pk>/delete', views.delete_status, name='delete_status'),  # noqa: E501
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/new/', views.TagCreate.as_view(), name='create_tag'),
]
