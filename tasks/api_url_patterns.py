from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/update-status/', views.task_update_status, name='task_update_status'),
]
