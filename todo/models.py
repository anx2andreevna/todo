from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название метки')

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название приоритета')

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    due_date = models.DateField(blank=True, null=True, verbose_name='Срок выполнения')
    completed = models.BooleanField(default=False, verbose_name='Завершено')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name='Приоритет')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, verbose_name='Метки')  # Многие-ко-многим с метками
    is_hidden = models.BooleanField('Скрыт', default=False)
    favorite = models.BooleanField('Избранное', default=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Ссылка на родительскую задачу
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    due_date = models.DateField(blank=True, null=True, verbose_name='Срок выполнения')
    completed = models.BooleanField(default=False, verbose_name='Завершено')

    def __str__(self):
        return self.title
class TaskUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Задача пользователя'
        verbose_name_plural = 'Задачи пользователей'

    def __str__(self):
        return f'{self.user.username} - {self.task.title}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
