from rest_framework import routers
from django.urls import path, include, re_path

app_name = 'myapp'

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]
