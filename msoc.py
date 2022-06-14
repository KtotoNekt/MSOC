from bs4 import BeautifulSoup
import requests
from threading import Thread
import json
from time import sleep

import app


url = "https://mp3-uk.net/"
music_urls = {}
threads = []

class Search():
    def search_music(self, music):
        response = requests.post(url, {
                    "do": "search",
                    "subaction": "search",
                    "story": music
                })

        doc = BeautifulSoup(response.text, "html.parser")

        for track in doc.find_all("div", {"class": "track-item"}):
            _t = Thread(target=self.add_widget_url, args=(track,))
            threads.append(_t)
            _t.start()
        
    def add_widget_url(self, track):
        _u = track.find("a", {"class": "track-dl"})["onclick"].split("url=")[1].split("'")[0]
        _doc = requests.get(_u).text

        if _doc.startswith("<!DOCTYPE html>"): 
            doc_music = BeautifulSoup(_doc, "html.parser")
            _u = doc_music.find("meta", {"http-equiv": "refresh"})["content"].split("?url=")[-1]

            _key = _u.split("?")[-1]
        else:
            _key = _u.split("&t=")[-1].replace("+", " ")

        _key = _key.replace(".mp3", "")
        # Расскоментируйте, если хотите вывод сокращенных ссылок
        # _u = short_url(_u, _key)
        
        music_urls[_key] = _u
        print("\n" + _key + ": " + _u + "\n")
        del threads[-1]

    # Функция для сокращение ссылок
    # def short_url(self, url, name):
    #     resp = requests.post("https://23usi.ru/", {
    #         "url": url,
    #         "submit": "Создать"
    #     })
    #     _html = BeautifulSoup(resp.text, "html.parser")
    #     url_short = _html.find("div", {"id": "urlText"})
    #     if url_short:
    #         return url_short.text
    #     else:
    #         with open("crash.txt", "a") as fa:
    #             fa.write(name + ": " + url)
    #         return "Ошибка в ссылке, полная ссылка для скачивания в файле crash.txt"


def listen_music(host="127.0.0.1"):
    with open("musics.json", "w") as fw:
        json.dump(music_urls, fw)

    app.app.run(host, "4165")

print("-------------------------------")
print("MSOC (Music Search On Console)")
print("-------------------------------")

sear = Search()
while True:
    music_urls = {}
    music = input("Музыка($exit - выход): ")
    if music.lower() == "$exit":
        break

    sear.search_music(music)
    while True:
        sleep(3)
        if len(threads) == 0:
            if input("Хотите прослушать?[Y/n]: ").lower() != "n":
                is_localhost = input("Развернуть в локальной сети?[Y/n]: ")
                print("Что бы закрыть прослушивание и продолжить парсить музыку, нажмите Ctrl+C")
                if is_localhost.lower() != "n":
                    
                    listen_music("0.0.0.0")
                else:
                    listen_music()
            break
