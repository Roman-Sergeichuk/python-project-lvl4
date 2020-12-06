from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views


TASK_LIST = 'task_list'
TASK_CREATE = 'create_task'
TASK_UPDATE = 'update_task'
TASK_DELETE = 'delete_task'
TASK_DETAIL = 'task_detail'
STATUS_LIST = 'status_list'
STATUS_CREATE = 'create_status'
STATUS_UPDATE = 'update_status'
STATUS_DELETE = 'delete_status'
STATUS_DETAIL = 'status_detail'
TAG_LIST = 'tag_list'
TAG_CREATE = 'create_tag'
TAG_UPDATE = 'update_tag'
TAG_DELETE = 'delete_tag'
TAG_DETAIL = 'tag_detail'


urlpatterns = [
    path('', views.TaskListView.as_view(), name=TASK_LIST),
    path('new/', views.TaskCreate.as_view(), name=TASK_CREATE),
    path('<int:pk>/', views.TaskDetail.as_view(), name=TASK_DETAIL),
    path('<int:pk>/update', views.TaskUpdate.as_view(), name=TASK_UPDATE),
    path('<int:pk>/delete', views.TaskDelete.as_view(), name=TASK_DELETE),
    path('statuses/new/', staff_member_required()(views.TaskStatusCreate.as_view()), name=STATUS_CREATE),  # noqa: E501
    path('statuses/', staff_member_required()(views.TaskStatusList.as_view()), name=STATUS_LIST),  # noqa: E501
    path('statuses/<int:pk>/', staff_member_required()(views.TaskStatusDetail.as_view()), name=STATUS_DETAIL),  # noqa: E501
    path('statuses/<int:pk>/update/', staff_member_required()(views.TaskStatusUpdate.as_view()), name=STATUS_UPDATE),  # noqa: E501
    path('statuses/<int:pk>/delete/', staff_member_required()(views.TaskStatusDelete.as_view()), name=STATUS_DELETE),  # noqa: E501
    path('tags/', views.TagList.as_view(), name=TAG_LIST),
    path('tags/<int:pk>', views.TagDetail.as_view(), name=TAG_DETAIL),
    path('tags/new/', views.TagCreate.as_view(), name=TAG_CREATE),
    path('tags/<int:pk>/update', views.TagUpdate.as_view(), name=TAG_UPDATE),  # noqa: E501
    path('tags/<int:pk>/delete', views.TagDelete.as_view(), name=TAG_DELETE),  # noqa: E501
]
