from bs4 import BeautifulSoup
import requests
from .models import Music


def get_name_track(track):
    track_title = track.find("div", {"class": "track-title"})
    try:
        return track_title.find("span").text
    except:
        return track_title.text


class MSOC:
    def __init__(self):
        self.url = "https://mp3uks.ru/"
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
        unclean_url = track.find("a", {"class": "track-dl"})["href"]
        
        if "/dl.php?" in unclean_url:
            _u = "https://mp3uk.net" + unclean_url
        else:
            _u = "https:" + unclean_url

        try:
            if not Music.objects.filter(name=name, url=_u):
                m = Music.objects.create(name=name, url=_u)
            else:
                m = Music.objects.get(name=name, url=_u)

            self.musics.append(m)
        except Exception as ex:
            pass
