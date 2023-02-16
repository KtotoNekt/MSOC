from bs4 import BeautifulSoup
import requests
from threading import Thread
import json
from time import sleep
import sys

import app


url = "https://mp3-uk.net/"
music_urls = {}
threads = []


def search_music(music):
    response = requests.post(url, {
                "do": "search",
                "subaction": "search",
                "story": music
            })

    doc = BeautifulSoup(response.text, "html.parser")

    for track in doc.find_all("div", {"class": "track-item"}):
        _t = Thread(target=add_widget_url, args=(track,))
        threads.append(_t)
        _t.start()


def get_name_track(track):
    track_title = track.find("div", {"class": "track-title"})
    try:
        return track_title.find("span").text
    except:
        return track_title.text


def add_widget_url(track):
    name = get_name_track(track)
    _u = track.find("a", {"class": "track-dl"})["onclick"].split("url=")[1].split("'")[0]

    try:
        headers = requests.head(_u).headers
        location_file = headers.get("location")
        
        if location_file:
            _u = location_file
            
        music_urls[name] = _u
        print("\n" + name + ": " + _u + "\n")
    except Exception as ex:
        print(ex)
    
    del threads[-1]


def listen_music(host="127.0.0.1"):
    with open("musics.json", "w") as fw:
        json.dump(music_urls, fw)

    app.app.run(host, "4165")

print("-------------------------------")
print("MSOC (Music Search On Console)")
print("-------------------------------")


while True:
    music_urls = {}
    if len(sys.argv) > 1:
        music = " ".join(sys.argv[1:])
        sys.argv.clear()
    else:
        music = input("Музыка($exit - выход): ")

    if music.lower() == "$exit":
        break

    search_music(music)
    while True:
        sleep(3)
        if len(threads) == 0:
            if music_urls != {}:
                if input("Хотите прослушать?[Y/n]: ").lower() != "n":
                    is_localhost = input("Развернуть в локальной сети?[Y/n]: ")
                    print("Что бы закрыть прослушивание и продолжить парсить музыку, нажмите Ctrl+C")
                    if is_localhost.lower() != "n":
                        listen_music("0.0.0.0")
                    else:
                        listen_music()
            else:
                print(f"По запросу \"{music}\" ничего не найдено...")
                
            break
