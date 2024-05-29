"""

    ░█████╗░██╗░░░░░███████╗██╗░░██╗░░░░░██████╗░░█████╗░████████╗
    ██╔══██╗██║░░░░░██╔════╝╚██╗██╔╝░░░░░██╔══██╗██╔══██╗╚══██╔══╝
    ███████║██║░░░░░█████╗░░░╚███╔╝ ░░░░░██████╦╝██║░░██║░░░██║░░░
    ██╔══██║██║░░░░░██╔══╝░░░██╔██╗ ░░░░░██╔══██╗██║░░██║░░░██║░░░
    ██║░░██║███████╗███████╗██╔╝╚██╗░░░░░██████╦╝╚█████╔╝░░░██║░░░
    ╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░

    by CICADA, Cheroit, AK
"""

import asyncio
import logging
import os
import ssl
import re
import speech_recognition as sr
import requests

from pydub import AudioSegment

from time import sleep

from docx2pdf import convert

from pdf2docx import Converter

from io import BytesIO

from pytube import *
import moviepy
from moviepy.editor import *

from PIL import Image

import mimetypes


from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import adds.keyboards as kb

from config import bot_token

ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())


class States(StatesGroup):
    photo = State()
    format = State()
    link = State()
    resolution = State()
    voice_msg = State()


def bytes_to_megabytes(bytes_size):
    return bytes_size / (1024 ** 2)


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет! Тут потом будет текст для представления, '
                         'а пока, выбери что хочешь сделать)', reply_markup=kb.menu_keyboard)


@dp.message(F.text == "Конвертер")
async def converter_button(message: Message, state: FSMContext) -> None:
    await state.set_state(States.photo)
    await message.answer("Пришли фото или документ (файлом)")


@dp.message(States.photo, F.document)
async def handle_document(message: Message, state: FSMContext) -> None:
    document = message.document

    photo_formats = ['jpg', 'jpeg', 'png', 'webp']
    doc_formats = ['docx', 'pdf']

    file_format = (document.file_name.split('.')[-1]).lower()

    if file_format in photo_formats:
        await bot.download(document, document.file_name)

        photo_formats.remove(file_format)

        format_buttons = [
            [InlineKeyboardButton(text=photo_formats[0], callback_data=photo_formats[0])],
            [InlineKeyboardButton(text=photo_formats[1], callback_data=photo_formats[1])],
            [InlineKeyboardButton(text=photo_formats[2], callback_data=photo_formats[2])],
        ]

        format_keyboard = InlineKeyboardMarkup(inline_keyboard=format_buttons)

        await message.answer("Выберите формат для нового файла", reply_markup=format_keyboard)
        await state.update_data(photo=document.file_name)
        await state.set_state(States.format)

    elif file_format in doc_formats:
        await bot.download(document, document.file_name)

        if file_format == 'docx':
            convert(document.file_name, document.file_name.split('.')[0] + '.pdf')

            converted_file = FSInputFile(document.file_name.split('.')[0] + '.pdf')
            await bot.send_document(message.chat.id, converted_file, caption=f'💾 Ваш файл')

            os.remove(document.file_name)
            os.remove(document.file_name.split('.')[0] + '.pdf')

            await state.clear()
        else:
            cv = Converter(document.file_name)
            cv.convert(document.file_name.split('.')[0] + '.docx')
            cv.close()

            converted_file = FSInputFile(document.file_name.split('.')[0] + '.docx')
            await bot.send_document(message.chat.id, converted_file, caption=f'💾 Ваш файл')

            os.remove(document.file_name)
            os.remove(document.file_name.split('.')[0] + '.docx')

            await state.clear()
    else:
        await message.answer("Пожалуйста, пришлите фото или документ (файлом)")


@dp.callback_query(States.format, F.data == 'png')
async def to_png(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    path = data['photo']
    format_from = '.' + path.split('.')[-1]
    format_in = '.png'
    new_img = f'{path.replace(format_from, '')}1{format_in}'

    img = Image.open(path)
    img.save(new_img)

    converted_img = FSInputFile(new_img)
    await bot.send_document(callback.message.chat.id, converted_img, caption=f'📷 Ваше фото')

    os.remove(path)
    os.remove(new_img)

    await state.clear()


@dp.callback_query(States.format, F.data == 'jpg')
async def to_jpg(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)

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
    await bot.send_document(callback.message.chat.id, converted_img, caption=f'📷 Ваше фото')

    os.remove(path)
    os.remove(new_img)

    await state.clear()


@dp.callback_query(States.format, F.data == 'jpeg')
async def to_jpeg(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    path = data['photo']
    format_from = '.' + path.split('.')[-1]
    format_in = '.jpeg'
    new_img = f'{path.replace(format_from, '')}1{format_in}'

    img = Image.open(path)
    if format_from == '.png':
        img = img.convert('RGB')
    img.save(new_img)

    converted_img = FSInputFile(new_img)
    await bot.send_document(callback.message.chat.id, converted_img, caption=f'📷 Ваше фото')

    os.remove(path)
    os.remove(new_img)

    await state.clear()


@dp.callback_query(States.format, F.data == 'webp')
async def to_webp(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)

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
    await bot.send_document(callback.message.chat.id, converted_img, caption=f'📷 Ваше фото')

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

        youtube_object = YouTube(youtube_link)
        streams = youtube_object.streams
        file_name = youtube_object.title
        thumbnail_url = youtube_object.thumbnail_url

        set_of_res = sorted({res for stream in streams if (res := stream.resolution)
                             and int(res[:-1]) <= 720},key=lambda x: int(x[:-1]))
        builder = InlineKeyboardBuilder()

        for resolution in set_of_res:
            builder.button(text=resolution, callback_data=resolution)

        builder.button(text='Аудио', callback_data='audio')
        builder.adjust(5)

        response = requests.get(thumbnail_url)
        thumbnail_path = 'thumbnail.jpg'
        with open(thumbnail_path, 'wb') as file:
            file.write(response.content)

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_photo(message.chat.id, FSInputFile(thumbnail_path), caption=f'📹[{file_name}]({youtube_link})', reply_markup=builder.as_markup(), parse_mode='Markdown')

        os.remove(thumbnail_path)

        await state.update_data(link=youtube_link)
        await state.set_state(States.resolution)
    else:
        await message.answer('Кажется, это не ссылка на ютуб')


async def download_video(youtube_link: str, message: Message, resolution: str):
    loop = asyncio.get_event_loop()

    async def edit_message(progress_message: str):
        await message.edit_text(progress_message)

    def progress_func(stream, chunk, bytes_remaining):
        current = stream.filesize - bytes_remaining
        done = int(50 * current / stream.filesize)
        progress_message = (
            f"[{'=' * done}{' ' * (50 - done)}] "
            f"{bytes_to_megabytes(current):.2f} MB / {bytes_to_megabytes(stream.filesize):.2f} MB"
        )
        asyncio.run_coroutine_threadsafe(edit_message(progress_message), loop)

    youtube_object = YouTube(youtube_link, on_progress_callback=progress_func)
    streams = youtube_object.streams
    filtered_streams = streams.filter(res=resolution)
    stream = filtered_streams.first()

    video_title = stream.default_filename

    await loop.run_in_executor(None, stream.download)


@dp.callback_query(States.resolution)
async def download_any(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data == 'audio':
        data = await state.get_data()
        youtube_link = data['link']

        youtube_object = YouTube(youtube_link)
        youtube_object = youtube_object.streams.get_audio_only()

        video_title = youtube_object.default_filename[:-1] + '3'

        await callback.message.answer('Спасибо, пожалуйста подождите!')

        try:
            youtube_object.download(filename=video_title)
        except:
            await callback.message.answer('С вашим видео что-то не так')
            await state.clear()

        downloaded_audio = FSInputFile(video_title)
        await callback.message.answer('Ваше аудио:')
        await bot.send_document(chat_id=callback.message.chat.id, document=downloaded_audio)

        os.remove(video_title)

    else:
        resolution = callback.data
        data = await state.get_data()
        youtube_link = data['link']

        url = f'http://127.0.0.1:8081/bot{bot_token}/sendVideo'

        youtube_object = YouTube(youtube_link)
        streams = youtube_object.streams
        filtered_streams = streams.filter(res=resolution)
        stream = filtered_streams.first()
        mime_type = stream.mime_type

        video_title = stream.default_filename

        progress_message = await callback.message.reply('Спасибо, пожалуйста подождите!')

        await download_video(youtube_link, progress_message, resolution)
        await progress_message.edit_text("Загрузка завершена! Дождитесь отправки")

        clip = VideoFileClip(video_title)
        width, height = clip.size
        duration = clip.duration

        payload = {'chat_id': callback.message.chat.id,
                   'supports_streaming': 'true',
                   'width': width,
                   'height': height,
                   'duration': duration}

        files = [
            ('video', (video_title, open(video_title, 'rb'), mime_type))
        ]

        response = requests.post(url, data=payload, files=files)
        print(response.text)
        await callback.message.answer('Ваше видео! Что-нибудь еще?')

        os.remove(video_title)

    await state.clear()


@dp.message(F.voice)
async def translation_without_message(message: Message) -> None:
    voice_msg_id = message.voice.file_id

    file = await bot.get_file(voice_msg_id)
    file_path = file.file_path

    await bot.download_file(file_path, f'{message.from_user.id}_voice_message.ogg')

    audio = AudioSegment.from_ogg(f'{message.from_user.id}_voice_message.ogg')
    audio.export(f'{message.from_user.id}_voice_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(f'{message.from_user.id}_voice_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(f'"{text}" - расшифрованный текст')
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove(f'{message.from_user.id}_voice_message.ogg')
    os.remove(f'{message.from_user.id}_voice_message.wav')


@dp.message(F.text == "Расшифровать голосовое")
async def converter_button(message: Message, state: FSMContext) -> None:
    await state.set_state(States.voice_msg)
    await message.answer("Пришлите голосовое сообщение")


@dp.message(F.voice, States.voice_msg)
async def translation(message: Message, state: FSMContext) -> None:
    voice_msg_id = message.voice.file_id

    file = await bot.get_file(voice_msg_id)
    file_path = file.file_path

    await bot.download_file(file_path, f'{message.from_user.id}_voice_message.ogg')

    audio = AudioSegment.from_ogg(f'{message.from_user.id}_voice_message.ogg')
    audio.export(f'{message.from_user.id}_voice_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(f'{message.from_user.id}_voice_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(f'"{text}" - расшифрованный текст')
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove(f'{message.from_user.id}_voice_message.ogg')
    os.remove(f'{message.from_user.id}_voice_message.wav')

    await state.clear()


@dp.message(F.video_note)
async def translation_video_note(message: Message) -> None:
    note_msg_id = message.video_note.file_id
    file = await bot.get_file(note_msg_id)

    file_path = file.file_path

    await bot.download_file(file_path, f'{message.from_user.id}_video_note_message.mp4')

    mp4_file = f"{message.from_user.id}_video_note_message.mp4"
    mp3_file = f"{message.from_user.id}_video_note_message.mp3"

    video = moviepy.editor.VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(mp3_file)

    audio = AudioSegment.from_mp3(f"{message.from_user.id}_video_note_message.mp3")
    audio.export(f'{message.from_user.id}_video_note_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(f'{message.from_user.id}_video_note_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(f'"{text}" - расшифрованный текст')
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove(f'{message.from_user.id}_video_note_message.mp3')
    os.remove(f'{message.from_user.id}_video_note_message.wav')
    os.remove(f'{message.from_user.id}_video_note_message.mp4')


@dp.message(F.video_note, States.voice_msg)
async def translation_video_note(message: Message) -> None:
    note_msg_id = message.video_note.file_id
    file = await bot.get_file(note_msg_id)

    file_path = file.file_path

    await bot.download_file(file_path, f'{message.from_user.id}_video_note_message.mp4')

    mp4_file = f"{message.from_user.id}_video_note_message.mp4"
    mp3_file = f"{message.from_user.id}_video_note_message.mp3"

    video = moviepy.editor.VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(mp3_file)

    audio = AudioSegment.from_mp3(f"{message.from_user.id}_video_note_message.mp3")
    audio.export(f'{message.from_user.id}_video_note_message.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(f'{message.from_user.id}_video_note_message.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            await message.answer(f'"{text}" - расшифрованный текст')
        except sr.UnknownValueError:
            await message.answer("Извините, не удалось распознать речь.")
        except sr.RequestError as e:
            await message.answer(f"Произошла ошибка в распознавании речи: {e}")

    os.remove(f'{message.from_user.id}_video_note_message.mp3')
    os.remove(f'{message.from_user.id}_video_note_message.wav')
    os.remove(f'{message.from_user.id}_video_note_message.mp4')

    await state.clear()


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('error exit')
