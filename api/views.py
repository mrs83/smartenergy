from rest_framework import viewsets, routers
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsOwner
from .serializers import RoomSerializer, SensorSerializer, MeasurementSerializer, UserSerializer
from.filters import MeasurementDateFilter
from core.models import Room, Sensor, Measurement


__all__ = ('router',)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('room',)

    def get_queryset(self):
        return Sensor.objects.filter(user=self.request.user)


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    http_method_names = ('get', 'post')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('sensor', 'created')
    filter_class = MeasurementDateFilter

    def get_queryset(self):
        return Measurement.objects.filter(sensor__user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get',)


router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'sensors', SensorViewSet, base_name='sensor')
router.register(r'measurements', MeasurementViewSet, base_name='measurement')
router.register(r'users', UserViewSet)
