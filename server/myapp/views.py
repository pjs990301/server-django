from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

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
    user_info = Users.objects.filter(user_id=user_id).first()
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
