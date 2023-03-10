from bs4 import BeautifulSoup
import requests
from .models import Music


def get_name_track(track):
    track_title = track.find("div", {"class": "track-title"})
    try:
        return track_title.find("span").text
    except:
        return track_title.text


def check_url(url):
    new_url = url
    with requests.get(url, stream=True, timeout=10) as data:
        for content in data.iter_content(2048):
            content = str(content)
            if content.startswith("b'<!DOCTYPE html>") or content.startswith("b'<html>"):
                doc_music = BeautifulSoup(content, "html.parser")
                try:
                    new_url = doc_music.find("meta", {"http-equiv": "refresh"})["content"].split("?url=")[-1]
                except:
                    break

            return new_url

    return new_url


class MSOC:
    def __init__(self):
        self.url = "https://mp3-uk.net/"
        self.musics = []

    def search_music(self, music):
        response = requests.post(self.url, {
            "do": "search",
            "subaction": "search",
            "story": music
        })

        doc = BeautifulSoup(response.text, "html.parser")

        for track in doc.find_all("div", {"class": "track-item"}):
            self.add_widget_url(track)

        return self.musics

    def add_widget_url(self, track):
        name = get_name_track(track)
        _u = track.find("a", {"class": "track-dl"})["onclick"].split("url=")[1].split("'")[0]

        try:
            _u = check_url(_u)

            if not Music.objects.filter(name=name, url=_u):
                m = Music.objects.create(name=name, url=_u)
            else:
                m = Music.objects.get(name=name, url=_u)

            self.musics.append(m)
        except Exception as ex:
            pass
