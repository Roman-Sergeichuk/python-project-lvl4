from django.test import TestCase
from django.urls import reverse
from tasks.models import Tag, Task, TaskStatus
from django.contrib.auth.models import User
from django.test.client import Client
from django.utils import timezone
from django.contrib.auth import SESSION_KEY
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
USERNAME = REGISTRATION_DATA['username']
PASSWORD = REGISTRATION_DATA['password1']
LOGIN_DATA = {'username': USERNAME, 'password': PASSWORD}


class TaskManagerTestCase(TestCase):

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

    def test_create_status(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        client.post(LOGIN_URL, LOGIN_DATA, follow=True)
        response = client.post(STATUS_CREATE_URL, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(pk=1)
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
        statuses = TaskStatus.objects.all()
        self.assertEqual(statuses.count, 0)








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

