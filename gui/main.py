from kivy.app import App

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform

from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.core.clipboard import Clipboard
from kivy.config import Config
from kivy.network.urlrequest import UrlRequest

import requests
from bs4 import BeautifulSoup
from threading import Thread


Window.clearcolor = (.7, .8, .9, 1)
Config.set('kivy','window_icon','img/icon.ico')


class MSOGApp(App):

    def __init__(self):
        super().__init__()

        if platform == "android":
            self.text_input_font_size = 40
            self.btn_font_size = 20
        else:
            self.text_input_font_size = 20
            self.btn_font_size = 12

        self.text_input = TextInput(font_size=self.text_input_font_size, size_hint=[.7, 1])
        self.search_btn = Button(text="Искать", on_press=self.search_music, size_hint=[.26, 1],
                                 background_color=[0, 0, 1, .7])
        self.box_musics = GridLayout(cols=1, rows=10, size_hint=(1, .9), pos_hint={"top": .9, "right": 1})

        self.music_urls = {}
        self.musics_pages = []
        self.threads = []
        self.current_page = 0

        self.sound_name_playing = ""

        self.sound_playing = SoundLoader.load("sound.wav")

    def build(self):
        self.icon = 'icon.png'

        al = FloatLayout()

        bl = BoxLayout(orientation="horizontal", size_hint=[1, .1], pos_hint={"top": 1, "right": 1})
        bl.add_widget(self.text_input)
        bl.add_widget(self.search_btn)

        al.add_widget(bl)
        al.add_widget(self.box_musics)

        return al

    def copy_link(self, btn):
        Clipboard.copy(self.music_urls[btn.text])

    def change_musics_pages(self, btn):
        if btn.text == "Дальше":
            self.current_page += 1
        else:
            self.current_page -= 1

        self.box_musics.clear_widgets()
        self.show_page_musics()

    def create_musics_pages(self):
        count = 0
        musics = {}
        for k, v in self.music_urls.items():
            musics[k] = v
            count += 1

            if count == 10:
                self.musics_pages.append(musics)
                count = 0
                musics = {}

        if musics != {}:
            self.musics_pages.append(musics)

    def play_music(self, btn):
        if btn.text == "Play":
            if self.sound_playing.state != "stop":
                self.sound_playing.stop()
                
            if btn.ids["name"] == self.sound_name_playing:
                self.sound_playing.play()
            else:
                self.sound_name_playing = btn.ids["name"]

                with requests.get(btn.ids["url"], stream=True) as resp:
                    with open("sound.wav", "wb") as fw:
                        for chunk in resp.iter_content(chunk_size=8192):
                            fw.write(chunk)

                self.sound_playing = SoundLoader.load("sound.wav")
                if self.sound_playing:
                    self.sound_playing.play()

            self.change_text_widget(btn, "Stop")
        else:
            self.sound_playing.stop()
            self.change_text_widget(btn, "Play")

    def download_music(self, btn):
        if btn.text != "Done" and btn.text != "Downloading":
            Thread(target=self.download_thread, args=[btn,]).start()

            self.change_text_widget(btn, "Downloading")

    def change_text_widget(self, widget, text):
        widget.text = text

    def download_thread(self, btn):
        name = btn.ids["name"]
        url = btn.ids["url"]

        with requests.get(url, stream=True) as resp:
            with open(name + ".mp3", "wb") as fw:
                for chunk in resp.iter_content(chunk_size=8192):
                    fw.write(chunk)

        self.change_text_widget(btn, "Done")

    def show_page_musics(self):
        count = 0

        for k, v in self.musics_pages[self.current_page].items():
            count += 1

            box = BoxLayout()
            if self.current_page > 0 and count == 1:
                box.add_widget(Button(text="Назад", color="black", font_size=self.btn_font_size,
                                      on_press=self.change_musics_pages))
                self.box_musics.add_widget(box)
            elif count <= 9 or self.current_page == len(self.musics_pages)-1:
                box.add_widget(Button(text=k, color="black", on_press=self.copy_link, font_size=self.btn_font_size,
                                      background_color=[0, 0, 1, .4], size_hint=[.6, 1]))
                box.add_widget(Button(text="Play", color="black", on_press=self.play_music, font_size=self.btn_font_size,
                                      background_color=[0, 0, 1, .7], size_hint=[.2, 1], ids={"name": k, "url": v}))
                box.add_widget(Button(text="Download", color="black", font_size=self.btn_font_size,
                                      on_press=self.download_music, background_color=[0, 0, 1, .7], size_hint=[.2, 1],
                                      ids={"name": k, "url": v}))
                self.box_musics.add_widget(box)
            elif self.current_page != len(self.musics_pages)-1:
                box.add_widget(Button(text="Дальше", color="black", font_size=self.btn_font_size,
                                      on_press=self.change_musics_pages))
                self.box_musics.add_widget(box)
                break

    def search_music(self, e):
        if self.search_btn.text == "Искать" and self.text_input.text.strip() != "":
            self.sound_playing.stop()
            self.music_urls = {}
            self.musics_pages = []
            self.current_page = 0
            self.box_musics.clear_widgets()

            self.search_btn.text = "Идет поиск"
            music = self.text_input.text

            response = requests.post("https://mp3-uk.net/", {
                "do": "search",
                "subaction": "search",
                "story": music
            })

            doc = BeautifulSoup(response.text, "html.parser")
            tracks = doc.find_all("div", {"class": "track-item"})

            if tracks:
                for track in tracks:
                    _t = Thread(target=self.add_widget_url, args=(track,))
                    self.threads.append(_t)
                    _t.start()
            else:
                self.search_btn.text = "Ничего не найдено"
        elif self.search_btn.text == "Отобразить":
            self.create_musics_pages()
            self.show_page_musics()

            self.search_btn.text = "Искать"
        elif self.search_btn.text == "Ничего не найдено":
            self.search_btn.text = "Искать"

    def get_name_track(self, track):
        track_title = track.find("div", {"class": "track-title"})
        try:
            return track_title.find("span").text
        except:
            return track_title.text

    def add_widget_url(self, track):
        name = self.get_name_track(track)
        _u = track.find("a", {"class": "track-dl"})["onclick"].split("url=")[1].split("'")[0]

        try:
            with requests.get(_u, stream=True, timeout=10) as data:
                for content in data.iter_content(2048):
                    content = str(content)
                    if content.startswith("b'<!DOCTYPE html>") or content.startswith("b'<html>"):
                        doc_music = BeautifulSoup(content, "html.parser")
                        try:
                            _u = doc_music.find("meta", {"http-equiv": "refresh"})["content"].split("?url=")[-1]
                        except:
                            break

                    self.music_urls[name] = _u
                    break
        except:
            pass

        del self.threads[-1]

        if not self.threads:
            self.search_btn.text = "Отобразить"


MSOGApp().run()
