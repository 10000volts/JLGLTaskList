from django.db import models
from django.db.models import Q, Prefetch
from django.db import transaction

from utils.constants import TASK_STATUS, TASK_STATUS_CHOICES


class TaskList(models.Model):
    name = models.CharField(verbose_name=u'任务清单名称', max_length=128, unique=True)

    def __str__(self):
        return self.name


class TaskManager(models.Manager):
    def create_task(self, validated_data):
        """
        :param validated_data: {"name": "string"}
        :return:
        """
        with transaction.atomic():
            tl = validated_data.pop('tl')
            self.check_valid(validated_data)
            validated_data['status'] = TASK_STATUS.WAITING
            validated_data['tl'] = tl
            item = self.create(**validated_data)
            return item

    def check_valid(self, data):
        q = self.filter(**data).exists()
        if q:
            raise Exception("已存在同名任务~")


class Task(models.Model):
    objects = TaskManager()
    name = models.CharField(verbose_name=u'任务名称', max_length=128)
    status = models.PositiveSmallIntegerField(u'任务状态', default=TASK_STATUS.WAITING,
                                              choices=TASK_STATUS_CHOICES)
    tl = models.ForeignKey('tasklist.TaskList', on_delete=models.CASCADE,
                             related_name='task', verbose_name='任务所属清单')

    def __str__(self):
        return "{}:{} status:{}".format(self.tl.name, self.name, self.status)