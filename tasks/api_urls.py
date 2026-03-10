from django.urls import path
from . import api_views

urlpatterns = [
    path('tasks/', api_views.TaskListCreateAPI.as_view(), name='api_task_list'),
    path('tasks/<int:pk>/', api_views.TaskDetailAPI.as_view(), name='api_task_detail'),
]
