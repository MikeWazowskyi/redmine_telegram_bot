import logging
from django.db import models
from django_celery_beat.models import PeriodicTask

from redmine.models import RedmineGroup

logger = logging.getLogger(__name__)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Chat(models.Model):
    name = models.CharField(max_length=150, default='Default Chat')
    chat_id = models.BigIntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(RedmineGroup,
                                    related_name='groups_chats',
                                    through='ChatRedmineGroup')
    tasks = models.ManyToManyField(PeriodicTask,
                                   related_name='tasks',
                                   through='ChatTask', blank=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    published = ActiveManager()

    class Meta:
        verbose_name = 'Чат Telegram'
        verbose_name_plural = 'Чаты Telegram'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name


class ChatRedmineGroup(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    groups = models.ForeignKey(RedmineGroup, on_delete=models.CASCADE)


class ChatTask(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
