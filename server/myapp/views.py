from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .serializers import UserSerializer
from .serializers import ActivitySerializer
from .models import Users
from .models import Activity
from _datetime import datetime


class UserListViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class ActivityListViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    user_info = get_object_or_404(Users, user_id=user_id)
    if not user_info:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_info)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, user_id):
    activity_info = get_object_or_404(Activity, user_id=user_id)
    if not activity_info:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity_info)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitySerializer(activity_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityMonthStats(APIView):

    def get(self, request):
        fall_count = 0
        activity_count = 0
        speaker_count = 0
        warning_count = 0

        # RESTAPI Query GET
        user_id = request.GET.get('user_id', None)
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        # DB 질의
        queryset = Activity.objects.filter(user_id_id=user_id, date__year=year, date__month=month).values()

        # 해당 월 활동 통계 작성
        for count in queryset:
            fall_count += count['fall_count']
            activity_count += count['activity_count']
            speaker_count += count['speaker_count']
            warning_count += count['warning_count']

        activity_stats = {
                             'fall_count': fall_count,
                             'activity_count': activity_count,
                             'speaker_count': speaker_count,
                             'warning_count': warning_count,
        }

        return Response(activity_stats)
