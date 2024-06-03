import asyncio
from importlib import util
from os.path import dirname, join

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


def engines():
    return ENGINES.copy()


def load_search_engine(name, path_python_file: str):
    spec = util.spec_from_file_location(name, path_python_file)

    module = util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except:
        raise EnginePathNotFoundError(path_python_file)

    ENGINES[name] = module


def unload_search_engine(name):
    try:
        del ENGINES[name]
    except KeyError:
        raise LoadedEngineNotFoundError(name)


def __load_default_engines():
    for name, python_file_path in DEFAULT_ENGINES_MAP.items():
        load_search_engine(name, python_file_path)


async def search(query):
    tasks = []

    for engine in ENGINES.values():
        tasks.append(engine.search(query))

    for sound_future in asyncio.as_completed(tasks):
        sounds = await sound_future
        for sound in sounds:
            yield Sound(sound[0], sound[1])


__load_default_engines()