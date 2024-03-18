import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import adds.keyboards as kb

from config import bot_token


bot = Bot(token=bot_token)
dp = Dispatcher()


class States(StatesGroup):
    photo = State()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет! Тут потом будет текст для представления, '
                         'а пока, выбери что хочешь сделать)', reply_markup=kb.menu_keyboard)


@dp.message(F.text == "Конвертер")
async def converter_button(message: Message, state: FSMContext) -> None:
    await state.set_state(States.photo)
    await message.answer("Пришли мне фото (файлом!)")


@dp.message(States.photo, F.document)
async def handle_document(message: Message) -> None:
    document = message.document
    await bot.download(document, document.file_name)


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('error exit')

