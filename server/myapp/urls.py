from rest_framework import routers
from django.urls import path, include, re_path
from .views import UserViewSet
from .views import ActivityViewSet


app_name = 'myapp'

urlpatterns = [
    path('user', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('activity', ActivityViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]
