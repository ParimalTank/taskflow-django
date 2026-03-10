from django.urls import path
from . import views

urlpatterns = [
    path('', views.org_list, name='org_list'),
    path('create/', views.org_create, name='org_create'),
    path('<slug:slug>/', views.org_detail, name='org_detail'),
    path('<slug:slug>/edit/', views.org_edit, name='org_edit'),
    path('<slug:slug>/invite/', views.org_invite, name='org_invite'),
    path('<slug:slug>/remove/<int:user_id>/', views.org_remove_member, name='org_remove_member'),
    path('invitations/<int:pk>/accept/', views.invite_accept, name='invite_accept'),
    path('invitations/<int:pk>/decline/', views.invite_decline, name='invite_decline'),
]
