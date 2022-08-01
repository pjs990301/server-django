from rest_framework import routers
from django.urls import path, include, re_path

from .views import get,post

app_name = 'myapp'

urlpatterns = [
    path('/get_url', get, name='get'),
    path('/post_url', post, name='post'),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]
