from rest_framework import serializers
from .models import Users, RaspberryPi
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('user_id', 'date', 'warning_count', 'activity_count', 'speaker_count', 'fall_count')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('user_id', 'user_name', 'serial_number', 'mac_address')


class PiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaspberryPi
        fields = ('serial_number', 'mac_address', 'type')
