"""django_dubplates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django_dubplates.views import TrackViewSet, UserViewSet, api_root
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


tracks_all = TrackViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
track_detail = TrackViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('tracks/', tracks_all, name='tracks-all'),
    path('tracks/<int:pk>/', track_detail, name='track-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)