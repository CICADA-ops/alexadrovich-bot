import asyncio
import logging
import os

from PIL import Image

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

import adds.keyboards as kb

from config import bot_token


bot = Bot(token=bot_token)
dp = Dispatcher()


class States(StatesGroup):
    photo = State()
    format = State()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет! Тут потом будет текст для представления, '
                         'а пока, выбери что хочешь сделать)', reply_markup=kb.menu_keyboard)


@dp.message(F.text == "Конвертер")
async def converter_button(message: Message, state: FSMContext) -> None:
    await state.set_state(States.photo)
    await message.answer("Пришли фото (файлом)")


@dp.message(States.photo, F.document)
async def handle_document(message: Message, state: FSMContext) -> None:
    document = message.document
    photo_formats = ['jpg', 'png', 'webp']
    file_format = document.file_name.split('.')[-1]
    if file_format in photo_formats:
        await bot.download(document, document.file_name)

        photo_formats.remove(file_format)

        format_buttons = [
            [InlineKeyboardButton(text=photo_formats[0], callback_data=photo_formats[0])],
            [InlineKeyboardButton(text=photo_formats[1], callback_data=photo_formats[1])],
        ]

        format_keyboard = InlineKeyboardMarkup(inline_keyboard=format_buttons)

        await message.answer("Выберите формат для нового файла:", reply_markup=format_keyboard)
        await state.update_data(photo=document.file_name)
        await state.set_state(States.format)
    else:
        await message.answer("Пожалуйста, пришлите фото (файлом)")


@dp.callback_query(States.format, F.data == 'png')
async def to_png(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    path = data['photo']
    format_from = '.' + path.split('.')[-1]
    format_in = '.png'
    new_img = f'{path.replace(format_from, '')}1{format_in}'

    img = Image.open(path)
    img.save(new_img)

    converted_img = FSInputFile(new_img)
    await callback.message.answer('Ваше фото:')
    await bot.send_document(chat_id=callback.message.chat.id, document=converted_img)

    os.remove(path)
    os.remove(new_img)

    await state.clear()


@dp.callback_query(States.format, F.data == 'jpg')
async def to_jpg(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    path = data['photo']
    format_from = '.' + path.split('.')[-1]
    print(format_from)
    format_in = '.jpg'
    new_img = f'{path.replace(format_from, '')}1{format_in}'

    img = Image.open(path)
    if format_from == '.png':
        img = img.convert('RGB')
    img.save(new_img)

    converted_img = FSInputFile(new_img)
    await callback.message.answer('Ваше фото:')
    await bot.send_document(chat_id=callback.message.chat.id, document=converted_img)

    os.remove(path)
    os.remove(new_img)

    await state.clear()


@dp.callback_query(States.format, F.data == 'webp')
async def to_webp(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    path = data['photo']
    format_from = '.' + path.split('.')[-1]
    format_in = '.webp'
    new_img = f'{path.replace(format_from, '')}1{format_in}'

    img = Image.open(path)
    if format_from == '.png':
        img = img.convert('RGB')
    img.save(new_img)

    converted_img = FSInputFile(new_img)
    await callback.message.answer('Ваше фото:')
    await bot.send_document(chat_id=callback.message.chat.id, document=converted_img)

    os.remove(path)
    os.remove(new_img)

    await state.clear()


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('error exit')

