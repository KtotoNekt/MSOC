from msoc import *
import asyncio



async def main():
    # unload_search_engine("mp3uk")

    async for res in search(input()):
        print(res.url)


asyncio.run(main())
