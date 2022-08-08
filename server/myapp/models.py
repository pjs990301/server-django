import datetime

from django.db import models


def serial_default():
    return {'serial_number': [], 'type': []}


class Users(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True, unique=True)
    serial_number = models.JSONField(null=True, blank=True, default=serial_default)
    mac_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user_id


class Activity(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    warning_count = models.PositiveIntegerField(default=0)
    activity_count = models.PositiveIntegerField(default=0)
    speaker_count = models.PositiveIntegerField(default=0)
    fall_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user_id


class RaspberryPi(models.Model):
    type_choice = [
        (1, "Speaker"),
        (2, "CSI")
    ]
    serial_number = models.CharField(primary_key=True, max_length=200)
    mac_address = models.CharField(max_length=200)
    type = models.PositiveIntegerField(choices=type_choice)

    def __str__(self):
        return self.serial_number

