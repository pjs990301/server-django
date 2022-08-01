from rest_framework import serializers
from .models import Users
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('userId', 'date', 'warning_count', 'activity_count', 'speaker_count', 'fall_count')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('userId', 'userName')
