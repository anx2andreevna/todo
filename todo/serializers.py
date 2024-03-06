import datetime

from rest_framework import serializers
from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_due_date(self, value):
        if value and value < datetime.date.today():
            raise serializers.ValidationError("Дата не может быть в прошлом")
        return value

