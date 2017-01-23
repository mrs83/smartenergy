import datetime
from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone

from .models import Room, Sensor, Measurement


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
        self.tz = get_current_timezone()
        self.start_date = datetime.datetime.combine(self.today, datetime.time(0, 0, tzinfo=self.tz))
        self.end_date = datetime.datetime.combine(self.today, datetime.time(23, 59, tzinfo=self.tz))

        for sensor, data in self.measurements.items():
            for row in data:
                hours, mins = row[0]
                created = datetime.datetime.combine(self.today, datetime.time(hours, mins, tzinfo=self.tz))

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
        oven_total = Measurement.objects.get_total_for_sensor(self.oven, start_date=self.start_date,
                                                              end_date=self.end_date)
        self.assertEqual(oven_total, 7898.150000000001)

        dishwasher_total = Measurement.objects.get_total_for_sensor(self.dishwasher, start_date=self.start_date,
                                                                    end_date=self.end_date)
        self.assertEqual(dishwasher_total, 3549.48)

    def test_sensor_total(self):
        oven_total = self.oven.get_measurement_total(self.start_date, self.end_date)
        self.assertEqual(oven_total, 7898.150000000001)

        dishwasher_total = self.dishwasher.get_measurement_total(self.start_date, self.end_date)
        self.assertEqual(dishwasher_total, 3549.48)

    def tearDown(self):
        self.oven.delete()
        self.dishwasher.delete()
        self.room.delete()
        self.user.delete()
