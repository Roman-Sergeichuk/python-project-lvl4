from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from task_manager.urls import INDEX, REGISTER, LOGIN
from . import urls

from tasks.models import Tag, Task, TaskStatus


USERNAME = 'test_user'
PASSWORD = 'Efwefwef1223'
REGISTRATION_DATA = {
    'username': USERNAME,
    'password1': PASSWORD,
    'password2': PASSWORD}
LOGIN_DATA = {'username': USERNAME, 'password': PASSWORD}
STATUS_DATA = {'name': 'Новая'}
STATUS_NAME = STATUS_DATA['name']
TAG_NAME = 'new_tag'
TAG_DATA = {'name': TAG_NAME}

# task form fields:
TASK_NAME, TASK_DESCRIPTION, TASK_STATUS, TASK_ASSIGNED_TO, TASK_CREATOR, TASK_TAGS = (  # noqa: E501
    'name', 'description', 'status', 'assigned_to', 'creator', 'tags'
)


def create_user(is_staff):
    User.objects.create_user(username=USERNAME, password=PASSWORD)
    user = User.objects.get(username=USERNAME)
    user.is_staff = is_staff
    user.save()
    return user


def prepare_db(staff_user=False):
    TaskStatus.objects.create(name=STATUS_NAME)
    Tag.objects.create(name=TAG_NAME)
    status = TaskStatus.objects.get(name=STATUS_NAME)
    tag = Tag.objects.get(name=TAG_NAME)
    user = create_user(is_staff=staff_user)
    return status, tag, user


def create_and_get_task():
    Task.objects.create(name='test_task',
                        description='description',
                        status=TaskStatus.objects.get(name=STATUS_NAME),
                        creator=User.objects.get(username=USERNAME),
                        assigned_to=User.objects.get(username=USERNAME)
                        )
    return Task.objects.get(name='test_task')


def create_task_data(status, tag, user):
    task_data = {
        TASK_NAME: 'task_1',
        TASK_DESCRIPTION: 'description',
        TASK_STATUS: status.pk,
        TASK_ASSIGNED_TO: user.pk,
        TASK_CREATOR: user.pk,
        TASK_TAGS: [tag.pk],
    }
    return task_data


class TestRegisterAndLogin(TestCase):

    # User can register in system
    def test_register(self):
        client = Client()
        response = client.post(reverse(REGISTER), REGISTRATION_DATA, follow=True)
        user_in_db = User.objects.get(username=USERNAME)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(USERNAME, user_in_db.username)

    # Registered user can login
    def test_login(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        response = client.post(reverse(LOGIN), LOGIN_DATA, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)


class TestStatusCRUD(TestCase):

    # Authenticated staff user can create statuses
    def test_create_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        response = client.post(reverse(urls.STATUS_CREATE), STATUS_DATA)
        status_in_db = TaskStatus.objects.get(name=STATUS_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_NAME, status_in_db.name)

    # Authenticated staff user can update statuses
    def test_update_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_url = reverse(urls.STATUS_UPDATE, args=[str(old_status.pk)])
        response = client.post(status_url, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(pk=old_status.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_NAME, status_in_db.name)

    # Authenticated staff user can delete statuses
    def test_delete_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_delete_url = reverse(urls.STATUS_DELETE, args=[str(old_status.pk)])  # noqa: E501
        response = client.get(status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(TaskStatus.objects.all()), 0)


class TestTagCRUD(TestCase):

    # Any authenticated user can create tags
    def test_create_tag(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        response = client.post(reverse(urls.TAG_CREATE), TAG_DATA)
        tag_in_db = Tag.objects.get(name=TAG_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TAG_NAME, tag_in_db.name)

    # Any authenticated user can update tags
    def test_update_tag(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        Tag.objects.create(name='old_name')
        old_tag = Tag.objects.get(name='old_name')
        tag_update_url = reverse(urls.TAG_UPDATE, args=[str(old_tag.pk)])
        response = client.post(tag_update_url, TAG_DATA)
        tag_in_db = Tag.objects.get(pk=old_tag.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TAG_NAME, tag_in_db.name)

    # Any authenticated user can delete tags
    def test_delete_tag(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        Tag.objects.create(name='old_name')
        old_tag = Tag.objects.get(name='old_name')
        tag_delete_url = reverse(urls.TAG_DELETE, args=[str(old_tag.pk)])  # noqa: E501
        response = client.get(tag_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Tag.objects.all()), 0)


class TestTaskCRUD(TestCase):

    # Any authenticated user can create tasks
    def test_create_task(self):
        client = Client()
        status, tag, user = prepare_db()
        task_data = create_task_data(status, tag, user)
        client.force_login(user)
        response = client.post(reverse(urls.TASK_CREATE), task_data)
        task_in_db = Task.objects.get(name=task_data[TASK_NAME])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_data[TASK_NAME], task_in_db.name)

    # Any authenticated user can update tasks
    def test_update_task(self):
        client = Client()
        status, tag, user = prepare_db()
        client.force_login(user)
        old_task = create_and_get_task()
        task_update_data = create_task_data(status, tag, user)
        task_url = reverse(urls.TASK_UPDATE, args=[str(old_task.pk)])
        response = client.post(task_url, task_update_data)
        task_in_db = Task.objects.get(pk=old_task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_update_data[TASK_NAME], task_in_db.name)

    # Any authenticated user can delete tasks
    def test_delete_task(self):
        client = Client()
        status, tag, user = prepare_db()
        client.force_login(user)
        task = create_and_get_task()
        task_delete_url = reverse(urls.TASK_DELETE, args=[str(task.pk)])
        response = client.post(task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Task.objects.all()), 0)


class URLSTests(TestCase):

    #  All resources are available for the authenticated staff user
    def test_200_ok(self):
        client = Client()
        status, tag, user = prepare_db(staff_user=True)
        client.force_login(user)
        task = create_and_get_task()
        urls_200_ok = (
            reverse(urls.TASK_LIST), reverse(urls.STATUS_LIST), reverse(urls.TAG_LIST),  # noqa: E501
            reverse(urls.TASK_CREATE), reverse(urls.TAG_CREATE), reverse(LOGIN), reverse(REGISTER),  # noqa: E501
            reverse(urls.STATUS_DETAIL, args=[str(status.pk)]), reverse(urls.TASK_DETAIL, args=[str(task.pk)]),  # noqa: E501
            reverse(urls.TAG_DETAIL, args=[str(tag.pk)]), reverse(INDEX)
        )
        for url in urls_200_ok:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)


class PermissionsTest(TestCase):

    #  Some resources are not available for non-authenticated user
    def test_non_auth_access(self):
        client = Client()
        status, tag, user = prepare_db()
        task = create_and_get_task()
        urls_302 = (
            reverse(urls.TASK_LIST), reverse(urls.STATUS_LIST), reverse(urls.TAG_LIST),  # noqa: E501
            reverse(urls.TASK_CREATE), reverse(urls.TAG_CREATE), reverse(urls.TAG_DETAIL, args=[str(tag.pk)]),  # noqa: E501
            reverse(urls.STATUS_DETAIL, args=[str(status.pk)]), reverse(urls.TASK_DETAIL, args=[str(task.pk)])  # noqa: E501
        )
        for url in urls_302:
            response = client.get(url)
            self.assertEqual(response.status_code, 302)


class TestNonAdminPermissions(TestCase):

    #  Non-staff user can't create statuses
    def test_should_not_create_status(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        response = client.post(reverse(urls.STATUS_CREATE), STATUS_DATA)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(TaskStatus.objects.all()), 0)

    #  Non-staff user can't update statuses
    def test_should_not_update_status(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_url = reverse(urls.STATUS_UPDATE, args=[str(old_status.pk)])
        response = client.post(status_url, STATUS_DATA)
        status_in_db = TaskStatus.objects.get(pk=old_status.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('old_name', status_in_db.name)

    #  Non-staff user can't delete statuses
    def test_should_not_delete_status(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        TaskStatus.objects.create(name='old_name')
        old_status = TaskStatus.objects.get(name='old_name')
        status_delete_url = reverse(urls.STATUS_DELETE, args=[str(old_status.pk)])  # noqa: E501
        response = client.get(status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(TaskStatus.objects.all()), 1)
