# MSOC - Библиотека для быстрого и асинхронного поиска музыки

MSOC - это библиотека на Python для быстрого и асинхронного поиска музыки в Интернете. Она позволяет искать треки на различных музыкальных сайтах и возвращает информацию о найденных треках, включая их названия и ссылки на скачивание.

# Установка

Для установки библиотеки можно использовать pip:
```bash
pip install msoc
```

Так же можно установить из исходников:
```bash
git clone https://codeberg.org/Ktoto/MSOC.git

cd MSOC

pip install .
```

# Использование

Импортируйте модуль msoc и используйте функцию search() для поиска музыки:

```python
from msoc import search
import asyncio


async def main():
    query = input("Запрос: ")
    
    async for sound in search(query):
        print(f"Name: {sound.name}, URL: {sound.url}")


asyncio.run(main())
```

Функция `search()` принимает поисковый запрос в качестве аргумента и возвращает асинхронный генератор, который генерирует объекты `Sound` с информацией о найденных треках.

## Реализованные движки поиска

В настоящее время библиотека MSOC поддерживает следующие движки поиска:

- mp3uk: Поиск на сайте [mp3uks.ru](https://mp3uks.ru)
- zaycev_net: Поиск на сайте [zaycev.net](https://zaycev.net)

Вы можете добавлять новые движки поиска, создавая модули и загружая их с помощью функций `load_search_engine()` и `unload_search_engine()`.

## Exceptions

Библиотека MSOC определяет следующие исключения:

- `LoadedEngineNotFoundError`: Выбрасывается, когда движок поиска не был найден в загруженных движках.
- `EnginePathNotFoundError`: Выбрасывается, когда не удается импортировать движок поиска по указанному пути.

## Создание своих поисковых движков
Для создания собственных поисковых движков на Python вы можете использовать следующий подход:

1. Создайте новый Python-файл для вашего поискового движка:
   - Например, создайте файл my_search_engine.py.

2. Определите асинхронную функцию search(query), которая будет реализовывать поисковый алгоритм:
   - Функция search(query) должна возвращать список кортежей (name, url), где name - название найденного аудиофайла, а url - ссылка на его загрузку.
   - Реализуйте логику поиска, взаимодействуя с API или веб-страницами источников, которые вы хотите использовать.
   - Можете использовать библиотеки, такие как aiohttp, beautifulsoup4 и другие, для выполнения HTTP-запросов и парсинга HTML-страниц.

Функция `search` внутри движка должна возвращать список 
Пример реализации функции search(query) в my_search_engine.py:

```python
import aiohttp
from bs4 import BeautifulSoup


async def search(query: str) -> list[tuple[str, str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://example.com/search?q={query}") as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    results = []
    for item in soup.find_all("div", class_="search-result"):
        name = item.find("h3").text.strip()
        url = item.find("a")["href"]
        results.append((name, url))

    return results
```

3. Подключите ваш поисковый движок к системе:
   - В основном коде используйте функцию load_search_engine() для загрузки вашего движка:

```python
from msoc import load_search_engine, engines

load_search_engine("my_search_engine", "path/to/my_search_engine.py")
print(engines())
```
   - Замените "path/to/my_search_engine.py" на фактический путь к вашему файлу my_search_engine.py.
   - Далее вызываем `engines()`, чтобы удостовериться, что движок был успешно загружен

4. Теперь при запуске основной `search` функции, ваш движок будет автоматически загружен и использован для поиска песен

## Contribution

Если вы хотите внести свой вклад в развитие библиотеки MSOC, вы можете:

- Сообщить об ошибках или предложить новые функции
- Разработать и добавить новые движки поиска
- Улучшить документацию
- Исправить существующие проблемы
