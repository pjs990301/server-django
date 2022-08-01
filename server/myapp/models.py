import datetime

from django.db import models, __all__


# Create your models here.

class Users(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True, unique=True)
    user_name = models.CharField(max_length=100)

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
