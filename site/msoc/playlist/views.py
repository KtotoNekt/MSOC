from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import PlayListForm
from .models import PlayList
from main.models import Music


# Create your views here.
@login_required
def playlists_view(req):
    pls = PlayList.objects.filter(user=req.user)

    return render(req, 'playlist/playlists.html', {"playlists": pls})


@login_required
def add_to_playlist(req, playlist_id, music_id):
    playlist = PlayList.objects.get(id=playlist_id)

    if playlist.user == req.user:
        music = Music.objects.get(id=music_id)

        playlist.add_music(music)

        return redirect("random_music")

    raise Http404()


@login_required
def delete_to_playlist(req, playlist_id, music_id):
    playlist = PlayList.objects.get(id=playlist_id)
    if playlist.user == req.user:
        music = Music.objects.get(id=music_id)

        playlist.remove_music(music)

        referer = req.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)

        return redirect("main")

    raise Http404()


class PlayListDetailView(LoginRequiredMixin, DetailView):
    model = PlayList
    template_name = "playlist/view.html"
    context_object_name = "playlist"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            playlist = PlayList.objects.get(pk=pk)
            if playlist.user == request.user:
                return super().get(request, args, kwargs)
        except:
            pass

        raise Http404()


class PlayListUpdateView(LoginRequiredMixin, UpdateView):
    model = PlayList
    form_class = PlayListForm
    template_name = "playlist/update.html"
    success_url = "/playlists"
    context_object_name = "playlist"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            playlist = PlayList.objects.get(pk=pk)
            if playlist.user == request.user:
                return super().get(request, args, kwargs)
        except:
            pass

        raise Http404()


class PlayListDeleteView(LoginRequiredMixin, DeleteView):
    model = PlayList
    template_name = "playlist/delete.html"
    success_url = "/playlists"
    context_object_name = "playlist"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            playlist = PlayList.objects.get(pk=pk)
            if playlist.user == request.user:
                return super().get(request, args, kwargs)
        except:
            pass

        raise Http404()


class PlayListCreateView(LoginRequiredMixin, CreateView):
    model = PlayList
    template_name = "playlist/create.html"
    form_class = PlayListForm
    success_url = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


