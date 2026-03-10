from django.urls import path
from . import views

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('create/', views.board_create, name='board_create'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('<int:pk>/edit/', views.board_edit, name='board_edit'),
    path('<int:pk>/delete/', views.board_delete, name='board_delete'),
]
