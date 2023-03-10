from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from random import choice

from playlist.models import PlayList

from .msoc import MSOC, check_url
from .models import Music


def index(req):
    if req.POST:
        music_name = req.POST["music"]

        msoc = MSOC()

        musics = msoc.search_music(music_name)
        if req.user.is_authenticated:
            playlists = PlayList.objects.filter(user=req.user)
        else:
            playlists = []

        data = {
            "musics": musics,
            "value": music_name,
            "playlists": playlists
        }

        return render(req, 'main/index.html', data)

    return render(req, 'main/index.html')


def update_url_music(music: Music):
    new_url = check_url(music.url)
    if music.url != new_url:
        try:
            m = Music.objects.get(url=new_url)
            music.delete()
            print("Удалена:", music.id, music.name, music.url)

            print(m.name, m.url)
            return m
        except:
            print("Старая:", music.id, music.name, music.url)
            music.url = new_url
            print("Обновлена: ", music.id, music.name, music.url)
            music.save()

    return music


def last_search_music(req):
    musics = Music.objects.all().order_by("-pk")[:20]

    if not musics:
        return HttpResponse("<h1>Никто еще ничего не слушал</h1>")

    if req.user.is_authenticated:
        playlists = PlayList.objects.filter(user=req.user)
    else:
        playlists = []

    data = {
        "musics": musics,
        "playlists": playlists
    }

    return render(req, 'main/last-search.html', data)


def random_music(req):
    musics = Music.objects.all()

    if not musics:
        return HttpResponse("<h1>Никто еще ничего не слушал</h1>")

    music = update_url_music(choice(musics))

    if req.user.is_authenticated:
        playlists = PlayList.objects.filter(user=req.user)
        music_playlists = music.playlist.filter(user=req.user)
    else:
        playlists = []
        music_playlists = []

    data = {
        "music": music,
        "playlists": playlists,
        "music_playlists": music_playlists
    }

    return render(req, 'main/random-music.html', data)


def delete_music(req, music_id):
    if req.user.is_staff:
        try:
            music = Music.objects.get(id=music_id)
            music.delete()
        except:
            pass

        referer = req.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)

        return redirect("main")

    raise Http404()
