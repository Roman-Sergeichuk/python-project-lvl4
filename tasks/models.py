from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


NEW = 'Новая'


class TaskStatus(models.Model):

    name = models.CharField(
        max_length=50, unique=True,
        verbose_name='Статус',
        help_text='Введите статус',
        error_messages={'unique': 'Статус с таким названием уже существует'}
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('status_detail', args=[str(self.pk)])


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        error_messages={'unique': 'Тег с таким названием уже существует'}
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_detail', args=[str(self.pk)])


class Task(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        verbose_name='Статус')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор задачи'
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='assigned_to',
        on_delete=models.PROTECT,
        verbose_name='Исполнитель'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Теги')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.pk)])

