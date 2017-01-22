import datetime
from django.db import models
from django.contrib.auth.models import User
from macaddress.fields import MACAddressField


class BaseModel(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created']


class Room(BaseModel):
    name = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Sensor(BaseModel):
    room = models.ForeignKey(Room)
    name = models.CharField(max_length=35, blank=True)
    alias = models.CharField(max_length=35, blank=True)
    paired = models.NullBooleanField(blank=True)
    trusted = models.NullBooleanField(blank=True)
    blocked = models.NullBooleanField(blank=True)
    connected = models.NullBooleanField(blank=True)
    mac_address = MACAddressField(unique=True)
    user = models.ForeignKey(User)

    def get_measurement_estimate(self, start_date):
        return Measurement.objects.get_estimate_for_sensor(self, start_date)

    def get_measurement_total(self, start_date, end_date=None):
        return Measurement.objects.get_total_for_sensor(self, start_date, end_date)

    def get_all_measurement(self):
        return Measurement.objects.get_for_sensor(self)

    def __str__(self):
        return '{}: {}'.format(self.room, str(self.mac_address))


class MeasurementManager(models.Manager):
    def get_for_sensor(self, sensor):
        return self.filter(sensor=sensor)

    def get_estimate_for_sensor(self, sensor, date):
        queryset = self.get_for_sensor(sensor)
        before = queryset.filter(created__lte=date).order_by('-created').first()
        after = queryset.filter(created__gte=date).order_by('created').first()
        if not before and not after:
            return

        if not before:
            before = after
        elif not after:
            after = before

        if after.wh <= before.wh:
            return after.wh

        scale = (date - before.created).total_seconds() / (after.created - before.created).total_seconds()
        return (1 - scale) * before.wh + scale * after.wh

    def get_total_for_sensor(self, sensor, start_date, end_date=None):
        if not end_date:
            end_date = datetime.datetime.now()

        start = self.get_estimate_for_sensor(sensor, start_date)
        end = self.get_estimate_for_sensor(sensor, end_date)

        queryset = self.get_for_sensor(sensor).filter(created__gte=start_date, created__lte=end_date)

        measurements = list(queryset)
        if end:
            measurements.append(end)

        last_wh = None
        if start:
            last_wh = start.wh

        total = 0
        for m in measurements:
            if last_wh and m.wh >= last_wh:
                total += m.wh - last_wh
            else:
                total += m.wh

            last_wh = m.wh

        return total * 1000  # kWh


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor)
    wh = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    objects = MeasurementManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "{}: {} {}w".format(self.sensor, self.created, self.wh)
