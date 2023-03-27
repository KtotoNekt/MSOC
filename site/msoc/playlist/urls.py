from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", playlists_view, name="playlists"),
    path("create", PlayListCreateView.as_view(), name="create_playlist"),
    path("<int:pk>", PlayListDetailView.as_view(), name="view_playlist"),
    path("<int:pk>/delete", PlayListDeleteView.as_view(), name="delete_playlist"),
    path("<int:pk>/update", PlayListUpdateView.as_view(), name="update_playlist"),
    path("<int:playlist_id>/add/<int:music_id>", add_to_playlist, name="add_to_playlist"),
    path("<int:playlist_id>/del/<int:music_id>", delete_to_playlist, name="del_to_playlist"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)