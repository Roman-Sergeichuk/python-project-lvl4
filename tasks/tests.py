from django.test import TestCase
from django.urls import reverse
from tasks.models import Tag, Task, TaskStatus
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

REGISTRATION_DATA = {'username': 'test_user', 'password1': 'Efwefwef1223', 'password2': 'Efwefwef1223'}
REGISTER_URL = reverse_lazy('register')
LOGIN_URL = reverse_lazy('login')
STATUS_CREATE_URL = reverse_lazy('create_status')
STATUS_UPDATE_URL_NAME = 'update_status'
STATUS_DELETE_URL_NAME = 'delete_status'
STATUS_DATA = {'name': 'new'}
STATUS_NAME = STATUS_DATA['name']
TAG_CREATE_URL = reverse_lazy('create_tag')
TAG_DATA = {'name': 'Новая'}
TAG_NAME = TAG_DATA['name']
TASK_CREATE_URL = reverse_lazy('create_task')
TASK_DATA = {'name': 'task_1', 'description': 'description for task 1'}
TASK_UPDATE_URL_NAME = 'update_task'

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
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        response = client.post(STATUS_CREATE_URL, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(name=STATUS_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_NAME, status_in_db.name)

    def test_update_status(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
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
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_url = reverse(STATUS_DELETE_URL_NAME, args=[str(old_status.pk)])
        response = client.post(status_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(TaskStatus.objects.all()), 0)


class TestTagCreate(TestCase):

    def test_create_tag(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        response = client.post(TAG_CREATE_URL, TAG_DATA)
        tag_in_db = Tag.objects.get(name=TAG_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TAG_NAME, tag_in_db.name)


class TestTaskCRUD(TestCase):

    def test_create_task(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        status = TaskStatus.objects.get(name=STATUS_NAME)
        tag = Tag.objects.get(name=TAG_NAME)
        user = User.objects.get(username=USERNAME)
        response = client.post(TASK_CREATE_URL, {'name': 'task_1', 'description': 'description for task 1', 'status': status.pk, 'tags': tag.pk, 'Assigned_to': user.pk})
        print(response)
        # task_in_db = Task.objects.get(name='task_1')
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual('task_1', task_in_db.name)

    def test_update_task(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        TaskStatus.objects.create(name=STATUS_NAME)
        Tag.objects.create(name=TAG_NAME)
        Task.objects.create(name='task1',
                            description='description',
                            status=TaskStatus.objects.get(name=STATUS_NAME),
                            creator=User.objects.get(username=USERNAME),
                            assigned_to=User.objects.get(username=USERNAME)
                            )
        old_task = Task.objects.get(name='task1')
        task_url = reverse(TASK_UPDATE_URL_NAME, args=[str(old_task.pk)])
        task_update_data = {
            'name': 'task2',
            'description': 'description',
            'status': str(TaskStatus.objects.get(name=STATUS_NAME)),
            'assigned_to': str(User.objects.get(username=USERNAME))
        }
        response = client.post(task_url, task_update_data)
        task_in_db = TaskStatus.objects.get(pk=old_task.pk)
        print(task_in_db)

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(STATUS_NAME, status_in_db.name)



    # def test_can_create_task(self):
    #     """Пользователь может успешно создать статус"""
    #     default_user = User.objects.create(username='default_user', password="Efwefwef1223")
    #     c = Client()
    #     user = User.objects.get(pk=1)
    #     print(user.username)
    #     response1 = c.post('/accounts/login/', {'username': 'default_user', 'password': 'Efwefwef1223'})
    #     self.assertEqual(response1.status_code, 200)
        # print(response1.url)
        # c = Client()
        # response1 = c.get('')
        # print(response1.status_code)
        # self.assertEqual(response1.status_code, 200)


        # status_data = {
        #     "name": "Новая",
        # }
        #
        # response = self.client.post(
        #     path='/tasks/statuses/new/',
        #     data=status_data,
        # )

        # status_in_db = TaskStatus.objects.get(name=status_data['name'])
        # serializer = TaskSerializer(task_in_db)
        # print(response)
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual("Новая", status_in_db.name)

