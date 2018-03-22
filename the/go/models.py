from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save

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
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to="posts/",blank = True, null = True)

    def __str__(self):
        return self.user

    def save_profile(self):
        self.save()

    @classmethod
    def this_profile(cls):
        profile = cls.objects.all()
        return profile

def Create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(Create_profile,sender=User)
