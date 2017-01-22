from unittest import mock
import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Room, Sensor, Measurement


# datetime.datetime.combine(datetime.date(2011, 01, 01), datetime.time(10, 23))


class SmartEnergyTest(TestCase):
    measurements = {
        'oven': (
            ((6, 0), 1987.21),
            ((7, 0), 2010.41),
            ((8, 0), 2100.32),
            ((9, 0), 2001.62),
            ((10, 0), 1800.21),
        ),
        'dishwasher': (
            ((13, 0), 1198.32),
            ((14, 0), 1300.81),
            ((15, 0), 1050.35),
        )
    }

    def setUp(self):
        self.user = User.objects.create(
            username='user1'
        )
        self.room = Room.objects.create(
            name='Kitchen',
            description='Kitchen Room',
            user=self.user
        )
        self.oven = Sensor.objects.create(
            room=self.room,
            name='Smart Plug Sensor',
            alias='Oven',
            paired=True,
            trusted=True,
            blocked=True,
            connected=True,
            mac_address='01:23:45:67:89:ab',
            user=self.user
        )
        self.dishwasher = Sensor.objects.create(
            room=self.room,
            name='Smart Plug Sensor',
            alias='Dishwasher',
            paired=True,
            trusted=True,
            blocked=True,
            connected=True,
            mac_address='01:23:45:67:89:cd',
            user=self.user
        )
        self.today = datetime.date(2017, 1, 22)
        for sensor, data in self.measurements.items():
            for row in data:
                hours, mins = row[0]
                created = datetime.datetime.combine(self.today, datetime.time(hours, mins))

                # Mock timezone.now to set created for Measurement.
                with mock.patch('django.utils.timezone.now') as mock_now:
                    mock_now.return_value = created
                    Measurement.objects.create(
                        wh=row[1],
                        sensor=getattr(self, sensor)
                    )

    def test_measurement_estimate(self):
        pass

    def test_measurement_total(self):
        pass

    def tearDown(self):
        self.oven.delete()
        self.dishwasher.delete()
        self.room.delete()
        self.user.delete()
