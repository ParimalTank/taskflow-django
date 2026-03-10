from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:board_pk>/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
]
