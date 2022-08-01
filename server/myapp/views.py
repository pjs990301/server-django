from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from .serializers import ActivitySerializer
from .models import Users
from .models import Activity


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
