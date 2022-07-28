from rest_framework import viewsets
from .serializers import UserSerializer
from .serializers import ActivitySerializer
from .models import Users
from .models import Activity


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
