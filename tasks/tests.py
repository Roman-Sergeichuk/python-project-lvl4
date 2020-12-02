from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse, reverse_lazy

from tasks.models import Tag, Task, TaskStatus

REGISTRATION_DATA = {
    'username': 'test_user',
    'password1': 'Efwefwef1223',
    'password2': 'Efwefwef1223'}
INDEX_URL = reverse_lazy('index')
REGISTER_URL = reverse_lazy('register')
LOGIN_URL = reverse_lazy('login')
STATUS_CREATE_URL = reverse_lazy('create_status')
STATUS_LIST_URL = reverse_lazy('status_list')
STATUS_DETAIL_URL = reverse_lazy('status_detail', args=[str(1)])
STATUS_UPDATE_URL_NAME = 'update_status'
STATUS_DELETE_URL_NAME = 'delete_status'
STATUS_DATA = {'name': 'Новая'}
STATUS_NAME = STATUS_DATA['name']
TAG_CREATE_URL = reverse_lazy('create_tag')
TAG_LIST_URL = reverse_lazy('tag_list')
TAG_DATA = {'name': 'new_tag'}
TAG_NAME = TAG_DATA['name']
TASK_CREATE_URL = reverse_lazy('create_task')
TASK_LIST_URL = reverse_lazy('task_list')
TASK_UPDATE_URL_NAME = 'update_task'
TASK_DELETE_URL_NAME = 'delete_task'

USERNAME = REGISTRATION_DATA['username']
PASSWORD = REGISTRATION_DATA['password1']
LOGIN_DATA = {'username': USERNAME, 'password': PASSWORD}


class TestRegisterAndLogin(TestCase):

    def test_register(self):
        client = Client()
        response = client.post(REGISTER_URL, REGISTRATION_DATA, follow=True)
        user_in_db = User.objects.get(username=REGISTRATION_DATA['username'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_user", user_in_db.username)

    def test_login(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        response = client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)


class TestStatusCRUD(TestCase):

    def test_create_status(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        user.is_staff = True
        user.save()
        client.force_login(user)
        response = client.post(STATUS_CREATE_URL, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(name=STATUS_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_NAME, status_in_db.name)

    def test_update_status(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        user.is_staff = True
        user.save()
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_url = reverse(STATUS_UPDATE_URL_NAME, args=[str(old_status.pk)])
        response = client.post(status_url, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(pk=old_status.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_NAME, status_in_db.name)

    def test_delete_status(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        user.is_staff = True
        user.save()
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_delete_url = reverse(STATUS_DELETE_URL_NAME, args=[str(old_status.pk)])  # noqa: E501
        response = client.get(status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(TaskStatus.objects.all()), 0)


class TestTagCreate(TestCase):

    def test_create_tag(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        client.force_login(user)
        response = client.post(TAG_CREATE_URL, TAG_DATA)
        tag_in_db = Tag.objects.get(name=TAG_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TAG_NAME, tag_in_db.name)


class TestTaskCRUD(TestCase):

    def test_create_task(self):
        client = Client()
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        client.force_login(user)
        status = TaskStatus.objects.get(name=STATUS_NAME)
        tag = Tag.objects.get(name=TAG_NAME)
        task_create_data = {
            'name': 'task_1',
            'description': 'description',
            'status': status.pk,
            'assigned_to': user.pk,
            'creator': user.pk,
            'tags': [tag.pk],
        }
        response = client.post(TASK_CREATE_URL, task_create_data)
        task_in_db = Task.objects.get(name=task_create_data['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_create_data['name'], task_in_db.name)

    def test_update_task(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        client.force_login(user)
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        Task.objects.create(name='task1',
                            description='description',
                            status=TaskStatus.objects.get(name=STATUS_NAME),
                            creator=User.objects.get(username=USERNAME),
                            assigned_to=User.objects.get(username=USERNAME)
                            )
        old_task = Task.objects.get(name='task1')
        status = TaskStatus.objects.get(name=STATUS_NAME)
        tag = Tag.objects.get(name=TAG_NAME)
        task_url = reverse(TASK_UPDATE_URL_NAME, args=[str(old_task.pk)])
        task_update_data = {
            'name': 'task2',
            'description': 'description',
            'status': status.pk,
            'assigned_to': user.pk,
            'creator': user.pk,
            'tags': [tag.pk],
        }
        response = client.post(task_url, task_update_data)
        task_in_db = Task.objects.get(pk=old_task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_update_data['name'], task_in_db.name)

    def test_delete_task(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        client.force_login(user)
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        Task.objects.create(name='task1',
                            description='description',
                            status=TaskStatus.objects.get(name=STATUS_NAME),
                            creator=User.objects.get(username=USERNAME),
                            assigned_to=User.objects.get(username=USERNAME)
                            )
        task = Task.objects.get(name='task1')
        task_delete_url = reverse(TASK_DELETE_URL_NAME, args=[str(task.pk)])
        response = client.post(task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Task.objects.all()), 0)


class URLSTests(TestCase):

    def test_200_ok(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        user = User.objects.get(username=USERNAME)
        user.is_staff = True
        user.save()
        client.force_login(user)
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        Task.objects.create(name='task1',
                            description='description',
                            status=TaskStatus.objects.get(name=STATUS_NAME),
                            creator=User.objects.get(username=USERNAME),
                            assigned_to=User.objects.get(username=USERNAME)
                            )
        status = TaskStatus.objects.get(name=STATUS_NAME)
        Tag.objects.get(name=TAG_NAME)
        task = Task.objects.get(name='task1')
        status_detail_url = reverse('status_detail', args=[str(status.pk)])
        task_detail_url = reverse('task_detail', args=[str(task.pk)])
        urls_200_ok = (TASK_LIST_URL, STATUS_LIST_URL, TAG_LIST_URL,
                       TASK_CREATE_URL, TAG_CREATE_URL, LOGIN_URL, REGISTER_URL,
                       status_detail_url, task_detail_url)
        for url in urls_200_ok:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)



