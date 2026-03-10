from django.urls import path
from . import api_views

urlpatterns = [
    path('boards/', api_views.BoardListCreateAPI.as_view(), name='api_board_list'),
    path('boards/<int:pk>/', api_views.BoardDetailAPI.as_view(), name='api_board_detail'),
]
