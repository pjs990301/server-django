from rest_framework import routers
from django.urls import path, include, re_path

from .views import UserListViewSet
from .views import ActivityListViewSet

from .views import user_detail
from .views import activity_detail

from .views import ActivityMonthStats
app_name = 'myapp'

urlpatterns = [
    path('user/', UserListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('activity/', ActivityListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<slug:user_id>/', user_detail, name='user_detail'),
    path('activity/stats/', ActivityMonthStats.as_view(), name='activity_stats_detail'),
    path('activity/<slug:user_id>/', activity_detail, name='activity_detail'),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]

# urlpatterns = format_suffix_patterns (urlpatterns)
