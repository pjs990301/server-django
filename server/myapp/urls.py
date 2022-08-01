from rest_framework import routers
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserListViewSet
from .views import ActivityListViewSet

from .views import user_detail

app_name = 'myapp'

urlpatterns = [
    path('user/', UserListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('activity/', ActivityListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<slug:user_id>/', user_detail, name='user_detail'),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]

# urlpatterns = format_suffix_patterns (urlpatterns)

