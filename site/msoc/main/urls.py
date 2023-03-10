from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name='main'),
    path("last_search_music", last_search_music, name='last_search_music'),
    path("random_music", random_music, name="random_music"),
    path("delete_music/<int:music_id>", delete_music, name="delete_music"),
]
