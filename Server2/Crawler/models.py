from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

# Create your models here.
class FestaData(models.Model):
    title = models.CharField(max_length=200)
    time = models.CharField(max_length=40)
    price = models.CharField(max_length=30)
    url = models.CharField(max_length=128)
    def __str__(self):
        return self.title

class PiazzaData(models.Model):
    lecture = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    time = models.CharField(max_length=256)
    def __str__(self):
        return self.lecture

class MyUser(models.Model):
    id = models.CharField(max_length=512, primary_key=True)
    pw = models.CharField(max_length=512)
    push_token = models.CharField(max_length=256)

    def __str__(self):
        return self.push_token
