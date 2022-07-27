from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Users


class PostViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = PostSerializer

