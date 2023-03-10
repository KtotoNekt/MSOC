from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Music(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    playlist = models.ManyToManyField("playlist.PlayList")

    def __str__(self):
        return self.name

# from main.models import Music


