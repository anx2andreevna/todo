import datetime

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Task, TaskUser
from rest_framework import permissions

from .pagination import CustomPagination
from .serializers import CategorySerializer, TaskSerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from django_filters import rest_framework as rest_filters, CharFilter
from rest_framework import filters


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class UserViewSet(ModelViewSet):
    queryset = TaskUser.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination


    def get_queryset(self):
        user = self.request.user
        task_user = TaskUser.objects.get(user=user)
        return Task.objects.filter(taskuser=task_user)


class TaskFilter(rest_filters.FilterSet):
    category = CharFilter(field_name='category')

    class Meta:
        model = Task
        fields = ['category',]


class TaskViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination

    filterset_class = TaskFilter
    filter_fields = ['category',]
    ordering_fields = ['title', 'due_date']

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']

    @action(detail=True, methods=['POST'])



    def mark_as_favorite(self, request, pk=None):
        try:
            task = self.get_object()
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=404)

        task.favorite = True
        task.save()

        return Response({"message": f"Task '{task.title}' marked as favorite."}, status=200)

    @action(detail=False, methods=['GET'])
    def favorite_tasks(self, request):
        favorite_tasks = self.queryset.filter(favorite=True)
        serializer = self.get_serializer(favorite_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_tasks_priority(self, request):
        filter_tasks = self.queryset.filter((Q(completed=False) | Q(priority__gt=5)) & ~Q(category=1))
        serializer = self.get_serializer(filter_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_tasks_date(self, request):
        filter_tasks = self.queryset.filter(Q(category=1) & ~Q(completed=True) | Q(due_date__gte=datetime.date.today()))
        serializer = self.get_serializer(filter_tasks, many=True)
        return Response(serializer.data)



