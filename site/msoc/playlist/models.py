from django.contrib.auth import get_user_model
from django.db import models
from main.models import Music

User = get_user_model()

# Create your models here.
class PlayList(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def count_music(self):
        return len(self.list_music())

    def get_absolute_url(self):
        return f"/playlists/{self.id}"

    def list_music(self):
        return Music.objects.filter(playlist=self.id)

    def add_music(self, music):
        music.playlist.add(self)

    def remove_music(self, music):
        music.playlist.remove(self)


# from playlist.models import PlayList
