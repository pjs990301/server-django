from rest_framework import serializers
from .models import Users


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('userId', 'userName')
