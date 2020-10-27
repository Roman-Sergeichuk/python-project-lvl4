from django.db import models
from django.contrib.auth.models import User


class TaskStatus(models.Model):
    # STATUS_CHOICES = (
    #     ('NEW', 'Новая'),
    #     ('IN_THE_PIPELINE', 'В работе'),
    #     ('ON_TESTING', 'На тестировании'),
    #     ('COMPLETED', 'Завершено'),
    # )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_to', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
