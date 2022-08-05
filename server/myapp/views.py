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


@api_view(['GET'])
def activity_user_detail(request, user_id):
    if request.method == 'GET':
        activity_info = Activity.objects.filter(user_id=user_id).order_by('date')
        if not activity_info:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
def activity_user_change(request, user_id, year, month, day):
    if request.method == 'PUT':
        activity_info = Activity.objects.get(user_id_id=user_id, date__year=year, date__month=month,
                                             date__day=day)
        if not activity_info:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity_info = Activity.objects.get(user_id_id=user_id, date__year=year, date__month=month,
                                             date__day=day)
        if not activity_info:
            return Response(status=status.HTTP_404_NOT_FOUND)
        activity_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def activity_day_check(request, user_id, year, month, day):
    if request.method == 'POST':
        try:
            activity_info = Activity.objects.get(user_id_id=user_id, date__year=year, date__month=month,
                                                 date__day=day)
            return Response(status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            activity_data = {
                'user_id': user_id,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'fall_count': 0,
                'activity_count': 0,
                'speaker_count': 0,
                'warning_count': 0,
            }
            serializer = ActivitySerializer(data=activity_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # 질의를 찾지 못한 경우 404 NOT_FOUND return
        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 해당 월 활동 통계 작성
        for count in queryset:
            fall_count += count['fall_count']
            activity_count += count['activity_count']
            speaker_count += count['speaker_count']
            warning_count += count['warning_count']

        # dir 작성 (Json 전송)
        activity_stats = {
            'fall_count': fall_count,
            'activity_count': activity_count,
            'speaker_count': speaker_count,
            'warning_count': warning_count,
        }

        return Response(activity_stats, status=status.HTTP_200_OK)
