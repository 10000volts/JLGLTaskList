from tasklist.models import TaskList, Task
from rest_framework import serializers

from utils.mixins import CreateMixin, ParameterCheckMixin
from tasklist.models import TaskList, Task
from utils.constants import TASK_STATUS


class TaskBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status']
        read_only_fields = ['name']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status']
        read_only_fields = ['id', 'name', 'status']

    def update(self, instance, validated_data):
        instance.status = TASK_STATUS.ACCEPTED
        instance.save()
        return instance


class TaskCreateSerializer(serializers.ModelSerializer, CreateMixin):
    class Meta:
        model = Task
        fields = ['name', 'tl']

    def create(self, validated_data):
        return Task.objects.create_task(validated_data)


class TasklistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskList
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'tasklist-detail', 'lookup_field': 'id'},
            'owner': {'lookup_field': 'id'}
        }