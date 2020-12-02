from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    # path('', views.task_list, name='task_list'),
    path('', views.TaskListView.as_view(), name='task_list'),
    path('new/', views.TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update', views.TaskUpdate.as_view(), name='update_task'),
    path('<int:pk>/delete', views.delete_task, name='delete_task'),
    path('statuses/new/', staff_member_required()(views.TaskStatusCreate.as_view()), name='create_status'),  # noqa: E501
    path('statuses/', staff_member_required()(views.status_list), name='status_list'),  # noqa: E501
    path('statuses/<int:pk>', staff_member_required()(views.status_detail), name='status_detail'),  # noqa: E501
    path('statuses/<int:pk>/update', staff_member_required()(views.TaskStatusUpdate.as_view()), name='update_status'),  # noqa: E501
    path('statuses/<int:pk>/delete', staff_member_required()(views.delete_status), name='delete_status'),  # noqa: E501
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:pk>', views.tag_detail, name='tag_detail'),
    path('tags/new/', views.TagCreate.as_view(), name='create_tag'),
    path('tags/<int:pk>/update', views.TagUpdate.as_view(), name='update_tag'),  # noqa: E501
    path('tags/<int:pk>/delete', views.delete_tag, name='delete_tag'),  # noqa: E501

]
