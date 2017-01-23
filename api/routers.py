from rest_framework import routers

from .views import RoomViewSet, SensorViewSet, MeasurementViewSet, UserViewSet


__all__ = ('router',)


router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet, base_name='room')
router.register(r'sensors', SensorViewSet, base_name='sensor')
router.register(r'measurements', MeasurementViewSet, base_name='measurement')
router.register(r'users', UserViewSet)
