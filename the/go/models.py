from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save_location(self):
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length =500, blank= True)
