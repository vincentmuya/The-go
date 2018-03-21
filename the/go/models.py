from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharFIeld(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save_location(self):
        self.save()
