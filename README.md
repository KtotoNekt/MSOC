# MSOC - Библиотека для быстрого и асинхронного поиска музыки

MSOC - это библиотека на Python для быстрого и асинхронного поиска музыки в Интернете. Она позволяет искать треки на различных музыкальных сайтах и возвращает информацию о найденных треках, включая их названия и ссылки на скачивание.

## Структура проекта
```
├── msoc
│   ├── engines
│   │   └── mp3uk.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── msoc.py
│   └── sound.py
├── README.md
├── setup.py
└── test.py
```

## Использование

Импортируйте модуль msoc и используйте функцию search() для поиска музыки:

```python
from msoc import search

async def main():
    async for sound in search("my_query"):
        print(f"Name: {sound.name}, URL: {sound.url}")

asyncio.run(main())
```

Функция `search()` принимает поисковый запрос в качестве аргумента и возвращает асинхронный генератор, который генерирует объекты `Sound` с информацией о найденных треках.

## Реализованные движки поиска

В настоящее время библиотека MSOC поддерживает следующие движки поиска:

- mp3uk: Поиск на сайте [mp3uks.ru](https://mp3uks.ru)

Вы можете добавлять новые движки поиска, создавая модули и загружая их с помощью функций `load_search_engine()` и `unload_search_engine()`.

## Exceptions

Библиотека MSOC определяет следующие исключения:

- `LoadedEngineNotFoundError`: Выбрасывается, когда движок поиска не был найден в загруженных движках.
- `EnginePathNotFoundError`: Выбрасывается, когда не удается импортировать движок поиска по указанному пути.

## Contribution

Если вы хотите внести свой вклад в развитие библиотеки MSOC, вы можете:

- Сообщить об ошибках или предложить новые функции
- Разработать и добавить новые движки поиска
- Улучшить документацию
- Исправить существующие проблемы