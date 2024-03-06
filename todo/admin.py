from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources, fields
from import_export.formats import base_formats

from .models import Category, Task, Tag, Priority, TaskUser, Comment, SubTask
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ExportMixin


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TaskResource(resources.ModelResource):
    display_tags = fields.Field(column_name='tags')
    display_category = fields.Field(column_name='category')
    display_priority = fields.Field(column_name='priority')

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'display_priority',
            'display_tags',
            'display_category',
            'favorite',
            'is_hidden'
        )
        export_order = fields



    def get_export_queryset(self, request):
        qs = super().get_export_queryset(request)
        return qs.filter(completed=False)

    def dehydrate_display_tags(self, task):
        return ', '.join(tag.name for tag in task.tags.all())

    def dehydrate_display_category(self, task):
        return task.category.name if task.category else ""

    def dehydrate_display_priority(self, task):
        return task.priority.name if task.priority else ""



    # def before_export(self, queryset, *args, **kwargs):
    #     for obj in queryset:
    #         obj.display_status = "Active" if not obj.is_hidden else "Hidden"
    #     return super().before_export(queryset, *args, **kwargs)

@admin.register(Task)
class TaskAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, ExportMixin, admin.ModelAdmin):
    list_display = ('title', 'link_to_category', 'due_date', 'completed', 'display_tags', 'priority', 'favorite')
    list_filter = ('category', 'completed', 'due_date', 'priority', 'favorite', 'is_hidden')
    date_hierarchy = 'due_date'
    search_fields = ('title', 'description', 'tags__name')
    filter_horizontal = ('tags',)
    list_display_links = ('title',)
    raw_id_fields = ('category',)
    readonly_fields = ('display_tags',)
    inlines = [SubTaskInline]

    resource_class = TaskResource
    @admin.display(description='Метки')
    def display_tags(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())

    # display_tags.short_description = 'Метки'

    def link_to_category(self, obj):
        link = reverse("admin:todo_category_change", args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', link, obj.category.name)

    # link_to_category.short_description = 'Категория'

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('task', 'user')
    list_filter = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'created_at')
    list_filter = ('user', 'task', 'created_at')
    search_fields = ('user__username', 'task__title', 'text')
    list_per_page = 20
