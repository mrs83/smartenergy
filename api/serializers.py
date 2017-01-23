from rest_framework import serializers
from core.models import Sensor, Room, Measurement
from django.contrib.auth.models import User


__all__ = ('RoomSerializer', 'SensorSerializer', 'MeasurementSerializer', 'UserSerializer')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'user', 'created', 'updated')


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    paired = serializers.BooleanField()
    trusted = serializers.BooleanField()
    connected = serializers.BooleanField()
    blocked = serializers.BooleanField()
    estimate = serializers.ReadOnlyField()
    daily_total = serializers.ReadOnlyField()

    class Meta:
        model = Sensor
        fields = ('id', 'room', 'mac_address', 'name', 'alias', 'paired', 'trusted', 'connected', 'blocked', 'user',
                  'estimate', 'daily_total', 'created', 'updated')


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    wh = serializers.FloatField()

    class Meta:
        model = Measurement
        fields = ('id', 'sensor', 'wh', 'created')


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')
