from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo import views
from .api_views import CategoryViewSet, TaskViewSet, UserViewSet

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'category', CategoryViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('category/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.tasks_by_category, name='tasks_by_category'),
    path('tasks/', views.tasks_list, name='tasks_list'),

]
