from django.db import models


# Create your models here.

class Users(models.Model):
    userId = models.CharField(max_length=200)
    userName = models.CharField(max_length=100)

    def __str__(self):
        return self.userId
