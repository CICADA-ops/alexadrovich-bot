import asyncio
import logging
import aiohttp
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from adds.handlers import router

from config import bot_token


bot = Bot(token=bot_token)
dp = Dispatcher()


async def download_file(file_id: str):
    file_info = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url, ssl=False) as resp:
            if resp.status == 200:
                file_data = await resp.read()
                filename = os.path.basename(file_info.file_path)
                with open(filename, 'wb') as f:
                    f.write(file_data)
                return filename
            else:
                return None


async def start():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('error exit')

