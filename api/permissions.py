from rest_framework import permissions

from core.models import Room, Sensor, Measurement


__all__ = ('IsOwner',)


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit objects.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (Room, Sensor)):
            user  = obj.user
        elif isinstance(obj, Measurement):
            user = obj.sensor.user
        else:
            raise NotImplementedError

        return user == request.user
