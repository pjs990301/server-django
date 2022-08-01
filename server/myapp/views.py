from django.http import JsonResponse
from rest_framework import viewsets, permissions
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


class testView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return JsonResponse(status=200)


@api_view(['GET'])
def get(request):
    return Response(request)


@api_view(['POST'])
def post(request):
    return Response(request)
