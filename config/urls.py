from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('orgs/', include('organizations.urls')),
    path('orgs/<slug:slug>/boards/', include('boards.urls')),
    path('orgs/<slug:slug>/tasks/', include('tasks.urls')),
    path('tasks/', include('tasks.api_url_patterns')),  # AJAX status update
    path('api/', include('boards.api_urls')),
    path('api/', include('tasks.api_urls')),
    path('', lambda request: redirect('org_list')),
]
