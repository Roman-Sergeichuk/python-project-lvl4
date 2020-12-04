from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('new/', views.TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('<int:pk>/update', views.TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete', views.TaskDelete.as_view(), name='delete_task'),
    path('statuses/new/', staff_member_required()(views.TaskStatusCreate.as_view()), name='create_status'),  # noqa: E501
    path('statuses/', staff_member_required()(views.TaskStatusList.as_view()), name='status_list'),  # noqa: E501
    path('statuses/<int:pk>/', staff_member_required()(views.TaskStatusDetail.as_view()), name='status_detail'),  # noqa: E501
    path('statuses/<int:pk>/update/', staff_member_required()(views.TaskStatusUpdate.as_view()), name='update_status'),  # noqa: E501
    path('statuses/<int:pk>/delete/', staff_member_required()(views.TaskStatusDelete.as_view()), name='delete_status'),  # noqa: E501
    path('tags/', views.TagList.as_view(), name='tag_list'),
    path('tags/<int:pk>', views.TagDetail.as_view(), name='tag_detail'),
    path('tags/new/', views.TagCreate.as_view(), name='create_tag'),
    path('tags/<int:pk>/update', views.TagUpdate.as_view(), name='update_tag'),  # noqa: E501
    path('tags/<int:pk>/delete', views.TagDelete.as_view(), name='delete_tag'),  # noqa: E501

]
