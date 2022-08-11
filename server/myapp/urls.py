from rest_framework import routers
from django.urls import path, include

from .views import UserListViewSet, RaspberryPiListViewSet
from .views import ActivityListViewSet

from .views import user_detail
from .views import activity_user_detail
from .views import activity_user_change
from .views import activity_month_stats
from .views import activity_day_check
from .views import pi_register_user
from .views import pi_connected_check

app_name = 'myapp'

urlpatterns = [
    # 유저 생성 및 조회
    path('user/', UserListViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),

    # 유저 세부 사항 조회 및 수정
    path('user/<str:user_id>/', user_detail, name='user_detail'),

    path('activity/', ActivityListViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('activity/<str:user_id>/stats/<int:year>/<int:month>/', activity_month_stats, name='activity_stats_detail'),
    path('activity/check/<str:user_id>/<int:year>/<int:month>/<int:day>/', activity_day_check,
         name='activity_day_check'),
    path('activity/<str:user_id>/', activity_user_detail, name='activity_detail '),
    path('activity/<str:user_id>/<int:year>/<int:month>/<int:day>/', activity_user_change, name='activity_user_change'),

    # PI 정보 등록
    path('pi/', RaspberryPiListViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),

    # PI와 앱 동기화
    path('pi/<str:user_id>/<str:mac_address>/', pi_register_user, name="pi_register_user"),
    path('pi/check/<str:user_id>', pi_connected_check, name="pi_connected_check"),

    path('', include('rest_framework.urls', namespace='rest_framework_category')),
]
