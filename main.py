import asyncio
import logging
import os
import ssl
import re
import speech_recognition as sr

from pydub import AudioSegment

from time import sleep

from io import BytesIO

from pytube import *
import moviepy
from moviepy.editor import *

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

ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(token=bot_token)
dp = Dispatcher()


class States(StatesGroup):
    photo = State()
    format = State()
    link = State()
    type_of_download = State()
    voice_msg = State()


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
    file_format = (document.file_name.split('.')[-1]).lower()
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


@dp.message(F.text == "Скачать видео с Youtube")
async def youtube_downloader(message: Message, state: FSMContext) -> None:
    await state.set_state(States.link)
    await message.answer("Пожалуйста, пришлите ссылку на видео")


@dp.message(States.link)
async def getting_link(message: Message, state: FSMContext) -> None:
    youtube_link = message.text

    if ('youtu.be' in youtube_link) or ('youtube.com' in youtube_link) or ('m.youtube.com' in youtube_link):
        await message.answer('Теперь выберите что хотите скачать', reply_markup=kb.downloading_type_keyboard)
        await state.update_data(link=youtube_link)
        await state.set_state(States.type_of_download)
    else:
        await message.answer('Кажется, это не ссылка на ютуб')


@dp.callback_query(States.type_of_download, F.data == 'video')
async def video_download(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    youtube_link = data['link']

    youtube_object = YouTube(youtube_link)
    youtube_object = youtube_object.streams.get_highest_resolution()

    video_title = re.sub('[/:*?"<>|+.#]', '', youtube_object.title).replace('\\', '') + '.mp4'

    await callback.message.answer('Спасибо, пожалуйста подождите!')

    try:
        youtube_object.download()
    except:
        await callback.message.answer('С вашим видео что-то не так')
        await state.clear()

    while not (os.path.exists(video_title)):
        sleep(3)

    downloaded_video = FSInputFile(video_title)
    await callback.message.answer('Ваше видео:')
    await bot.send_document(chat_id=callback.message.chat.id, document=downloaded_video)

    os.remove(video_title)

    await state.clear()


@dp.callback_query(States.type_of_download, F.data == 'audio')
async def audio_download(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    print('Аудио')
    youtube_link = data['link']

    youtube_object = YouTube(youtube_link)
    youtube_object = youtube_object.streams.get_audio_only()

    video_title = re.sub('[/:*?"<>|+.#]', '', youtube_object.title).replace('\\', '') + '.mp3'

    await callback.message.answer('Спасибо, пожалуйста подождите!')

    try:
        youtube_object.download(filename=video_title)
    except:
        await callback.message.answer('С вашим видео что-то не так')
        await state.clear()

    while not (os.path.exists(video_title)):
        sleep(3)

    downloaded_audio = FSInputFile(video_title)
    await callback.message.answer('Ваше аудио:')
    await bot.send_document(chat_id=callback.message.chat.id, document=downloaded_audio)

    os.remove(video_title)

    await state.clear()


@dp.message(F.voice)
async def translation_without_message(message: Message) -> None:

    voice_msg_id = message.voice.file_id

    file = await bot.get_file(voice_msg_id)
    file_path = file.file_path

    await bot.download_file(file_path, 'voice_message.ogg')

    audio = AudioSegment.from_ogg('voice_message.ogg')
    audio.export('voice_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(text)
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove('voice_message.ogg')
    os.remove('voice_message.wav')

    await message.answer("Ваше расшифрованное сообщение выше")


@dp.message(F.text == "Расшифровать голосовое")
async def converter_button(message: Message, state: FSMContext) -> None:
    await state.set_state(States.voice_msg)
    await message.answer("Пришлите голосовое сообщение")


@dp.message(F.voice, States.voice_msg)
async def translation(message: Message, state: FSMContext) -> None:
    voice_msg_id = message.voice.file_id

    file = await bot.get_file(voice_msg_id)
    file_path = file.file_path

    await bot.download_file(file_path, 'voice_message.ogg')

    audio = AudioSegment.from_ogg('voice_message.ogg')
    audio.export('voice_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(text)
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove('voice_message.ogg')
    os.remove('voice_message.wav')

    await state.clear()
    await message.answer("Ваше расшифрованное сообщение выше")


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('error exit')
