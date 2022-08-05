from rest_framework import routers
from django.urls import path, include

from .views import UserListViewSet
from .views import ActivityListViewSet

from .views import user_detail
from .views import activity_user_detail
from .views import activity_user_change
from .views import activity_month_stats
from .views import activity_day_check

from .views import ActivityMonthStats

app_name = 'myapp'

urlpatterns = [
    path('user/', UserListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<str:user_id>/', user_detail, name='user_detail'),

    path('activity/', ActivityListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('activity/stats/<str:user_id>/<int:year>/<int:month>/', activity_month_stats, name='activity_stats_detail'),
    path('activity/day-check/<str:user_id>/<int:year>/<int:month>/<int:day>/', activity_day_check, name='activity_day_check'),
    path('activity/<str:user_id>/', activity_user_detail, name='activity_detail '),
    path('activity/<str:user_id>/<int:year>/<int:month>/<int:day>/', activity_user_change, name='activity_user_change'),

    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]

# urlpatterns = format_suffix_patterns (urlpatterns)
