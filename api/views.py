from rest_framework import viewsets, routers
from core.models import Room, Sensor, Measurement
from django.contrib.auth.models import User
from .serializers import RoomSerializer, SensorSerializer, MeasurementSerializer, UserSerializer


__all__ = ('router',)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get',)


router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'users', UserViewSet)
