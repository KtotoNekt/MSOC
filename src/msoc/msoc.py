import asyncio
from importlib import util
from os.path import dirname, join
from types import ModuleType
from typing import AsyncGenerator, Any

from .exceptions import *
from .sound import Sound


__all__ = [
    "search",
    "engines",
    "load_search_engine",
    "unload_search_engine",
    "Sound"
]


def __get_path_default_search_engine(engine_file: str):
    return join(dirname(__file__), "engines", engine_file)


ENGINES = dict()
DEFAULT_ENGINES_MAP = {
    "mp3uk": __get_path_default_search_engine("mp3uk.py"),
    "zaycev_net": __get_path_default_search_engine("zaycev_net.py")
}


def engines() -> dict[str, ModuleType]:
    """
    Функция возвращает словарь загруженных поисковых движков.
    """
    return ENGINES.copy()


def load_search_engine(name: str, path_python_file: str) -> None:
    """
    Функция загружает поисковой движок по путю к python файлу.

    Exceptions: EnginePathNotFoundError
    """
    spec = util.spec_from_file_location(name, path_python_file)

    module = util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except:
        raise EnginePathNotFoundError(path_python_file)

    ENGINES[name] = module


def unload_search_engine(name: str) -> None:
    """
    Функция удаляет поисковой движок из загруженных по name

    Exceptions: LoadedEngineNotFoundError
    """
    try:
        del ENGINES[name]
    except KeyError:
        raise LoadedEngineNotFoundError(name)


def __load_default_engines():
    for name, python_file_path in DEFAULT_ENGINES_MAP.items():
        load_search_engine(name, python_file_path)


async def consume(a_iter):
    try:
        return await a_iter.__anext__(),  asyncio.create_task(consume(a_iter))
    except StopAsyncIteration:
        return None, None


def create_generator_task(gen: AsyncGenerator) -> AsyncGenerator:
    result_queue = asyncio.create_task(consume(gen.__aiter__()))
    async def consumer():
        nonlocal result_queue
        while 1:
            item, result_queue = await result_queue
            if result_queue is None:
                assert item is None
                return
            yield item
    return consumer()



async def search(query: str):
    """
    Функция начинает поиск песен по запросу query.

    Возвращает: асинхронный генератор Sound
    """

    tasks = [
        create_generator_task(engine.search(query)) 
        for engine in ENGINES.values()
        ]

    for task in tasks:
        async for sound in task:
            yield sound
    

__load_default_engines()
