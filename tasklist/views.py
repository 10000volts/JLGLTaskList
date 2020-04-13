from django.shortcuts import render
from rest_framework import generics, viewsets, permissions  # , authentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from utils.swagger import DocParam

from tasklist.models import TaskList, Task
from tasklist.serializers import TaskBaseSerializer,\
    TaskCreateSerializer, TaskUpdateSerializer
from utils.mixins import ParameterCheckMixin


class TaskListView(generics.ListAPIView, ParameterCheckMixin):
    serializer_class = TaskBaseSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        lid = self.check_int_param('lid', required=True, post=False)
        tl = TaskList.objects.get(id=lid)
        return Task.objects.filter(tl=tl)


class TaskCreateView(generics.CreateAPIView, ParameterCheckMixin):
    serializer_class = TaskCreateSerializer
    permission_classes = (AllowAny,)


class TaskUpdateView(generics.UpdateAPIView, ParameterCheckMixin):
    serializer_class = TaskUpdateSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Task.objects.all()


class TaskDestroyView(generics.DestroyAPIView, ParameterCheckMixin):
    serializer_class = TaskBaseSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Task.objects.all()
