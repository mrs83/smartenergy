from rest_framework import serializers
from core.models import Sensor, Room, Measurement
from django.contrib.auth.models import User


__all__ = ('RoomSerializer', 'SensorSerializer', 'MeasurementSerializer', 'UserSerializer')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'description', 'user', 'created', 'updated')


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ('room', 'mac_address', 'name', 'alias', 'paired', 'trusted', 'connected', 'blocked', 'user',
                  'created', 'updated')


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = ('sensor', 'wh', 'created')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
