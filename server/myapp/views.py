from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, PiSerializer
from .serializers import ActivitySerializer
from .models import Users, RaspberryPi
from .models import Activity
from _datetime import datetime


class UserListViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class ActivityListViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class RaspberryPiListViewSet(viewsets.ModelViewSet):
    queryset = RaspberryPi.objects.all()
    serializer_class = PiSerializer


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
            if not activity_info:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
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


@api_view(['GET'])
def activity_month_stats(request, user_id, year, month):
    fall_count = 0
    activity_count = 0
    speaker_count = 0
    warning_count = 0

    if request.method == 'GET':
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

        # dir 작성 (JSON 전송)
        activity_stats = {
            'fall_count': fall_count,
            'activity_count': activity_count,
            'speaker_count': speaker_count,
            'warning_count': warning_count,
        }

        return Response(activity_stats, status=status.HTTP_200_OK)


@api_view(['PUT'])
def pi_register_user(request, user_id, mac_address):
    if request.method == 'PUT':

        # 같은 mac address 가지고 user, raspberrypi table 질의 => mac 주소가 같은 컬럼 뽑음
        # mac address 통해서 질의
        try:
            pi_info = RaspberryPi.objects.get(mac_address=mac_address)
            if not pi_info:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # mac address 통해서 질의
            user_info = Users.objects.get(user_id=user_id, mac_address=mac_address)
            if not user_info:
                return Response(status=status.HTTP_404_NOT_FOUND)
            print(pi_info.mac_address)
            print(user_info.mac_address)
            # User 정보에 PI 정보를 추가해 PUT
            if pi_info.mac_address == user_info.mac_address:
                serializer = UserSerializer(user_info, data={
                    "user_id": user_info.user_id,
                    "serial_number": {
                        "serial_number": pi_info.serial_number,
                        "type": pi_info.type
                    },
                    "mac_address": mac_address
                })
                # User 정보 저장
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except pi_info.DoesNotExist or user_info.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def pi_change_user(request, user_id, serial_number, mac_address, usage_type):
    if request.method == 'PUT':
        pi_info = RaspberryPi.objects.get(serial_number=serial_number)
        if not pi_info:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_info = Users.objects.get(user_id=user_id, serial_number__serial_number=serial_number)
        if not user_info:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # User 정보 수정
        if pi_info.serial_number == user_info.serial_number['serial_number']:
            serializer = UserSerializer(user_info, data={
                "user_id": user_info.user_id,
                "serial_number": {
                    "serial_number": serial_number,
                    "type": usage_type
                },
                "mac_address": mac_address
            })
            # User 정보 다시 넣기
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def pi_connected_check(request, user_id, mac_address):
    if request.method == 'GET':
        try:
            pi_info = RaspberryPi.objects.get(mac_address=mac_address)
            if not pi_info:
                return Response(status=status.HTTP_404_NOT_FOUND)

            user_info = Users.objects.get(user_id=user_id, mac_address=mac_address)
            if not user_info:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_200_OK)

        except pi_info.DoesNotExist or user_info.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
