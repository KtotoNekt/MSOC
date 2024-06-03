from msoc import search, engines
import asyncio


async def main():
    # query = input("Запрос: ")
    
    async for sound in search(1):
        print(f"Name: {sound.name}, URL: {sound.url}")


asyncio.run(main())