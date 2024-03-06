import datetime
import json

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Category, Task, TaskUser
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from django.http import HttpResponse
from rest_framework import permissions, generics
from .serializers import CategorySerializer, TaskSerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import filters


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def category_list(request):
    categories = Category.objects.all()
    tasks = Task.objects.all()
    return render(request, 'todo/category_list.html', {'categories': categories, 'tasks': tasks})

def tasks_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo/tasks_list.html', {'tasks': tasks})

def tasks_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = Task.objects.filter(
        Q(category=category) &
        Q(is_hidden=False)
    )
    tasks__notcompleted = Task.objects.filter(
        Q(category=category) &
        Q(completed=False)
    )
    tasks__completed = Task.objects.filter(
        Q(category=category) &
        Q(completed=True)
    )


    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.category = category
            task.save()
            return redirect('tasks_by_category', category_id=category_id)
    else:
        form = TaskForm()

    return render(request, 'todo/tasks_by_category.html', {'category': category, 'tasks': tasks, 'tasks__completed': tasks__completed, 'tasks__notcompleted': tasks__notcompleted, 'form': form})


