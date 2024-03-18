#import sr
#from aiogram import Bot, Dispatcher, types, F
#from aiogram.filters import CommandStart
#import speech_recognition as sr

#бот конвертор мп3 в текст -
'''TOKEN = '6854256929:AAEVLtamH3cCbQo4Y_IGhJ4M7Cv97ygDBzc'
bot = Bot(TOKEN)
dp = Dispatcher()
r = sr.Recognizer()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Привет! Отправь мне аудиофайл и я конвертирую его в текст!')


@dp.message(F.audio)
async def converting_audio_to_text(message: types.Message):
    split_tup = os.path.splitext(message.audio.file_name)
    file_name = f'{split_tup[0]}_{message.from_user.full_name}{split_tup[1]}'
    await bot.download(message.audio.file_id, file_name)

    file_name_wav = f'{split_tup[0]}_{message.from_user.full_name}.wav'
    subprocess.call([r'ffmpeg', '-i', file_name, file_name_wav])

    with sr.AudioFile(file_name_wav) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ru')
    await message.answer(text)

    os.remove(file_name)
    os.remove(file_name_wav)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())'''

#прога для работы с файлами -
'''from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import subprocess
import json
import os

import zipfile

with zipfile.ZipFile('model.zip', 'r') as zip_ref:
    zip_ref.extractall()
with zipfile.ZipFile('recasepunc.zip', 'r') as zip_ref:
    zip_ref.extractall()

SetLogLevel(0)

# Проверяем наличие модели
if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

# Устанавливаем Frame Rate
FRAME_RATE = 16000
CHANNELS=1

model = Model("model")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

#AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"

# Используя библиотеку pydub делаем предобработку аудио
mp3 = AudioSegment.from_mp3('Song.mp3')
mp3 = mp3.set_channels(CHANNELS)
mp3 = mp3.set_frame_rate(FRAME_RATE)

# Преобразуем вывод в json
rec.AcceptWaveform(mp3.raw_data)
result = rec.Result()
text = json.loads(result)["text"]

# Добавляем пунктуацию
cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)

# Записываем результат в файл
with open('res.txt', 'w') as f:
    json.dump(cased, f, ensure_ascii=False, indent=4)'''

"""
Telegram бот для конвертации голосового/аудио сообщения в текст.
"""
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from stt import STT
#from tts import TTS

load_dotenv()

TELEGRAM_TOKEN = "6854256929:AAEVLtamH3cCbQo4Y_IGhJ4M7Cv97ygDBzc"

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота
#tts = TTS()
stt = STT()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)


# Хэндлер на команду /start , /help
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это Бот для конвертации голосового/аудио сообщения в текст"
        " и создания аудио из текста."
    )


# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    """
    Обработчик команды /test
    """
    await message.answer("Test")


# Хэндлер на получение текста
'''@dp.message_handler(content_types=[types.ContentType.TEXT])
async def cmd_text(message: types.Message):
    """
    Обработчик на получение текста
    """
    await message.reply("Текст получен")

    out_filename = tts.text_to_ogg(message.text)

    # Отправка голосового сообщения
    path = Path("", out_filename)
    voice = InputFile(path)
    await bot.send_voice(message.from_user.id, voice,
                         caption="Ответ от бота")

    # Удаление временного файла
    os.remove(out_filename)'''


# Хэндлер на получение голосового и аудио сообщения
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
    ]
)
async def voice_message_handler(message: types.Message):
    """
    Обработчик на получение голосового и аудио сообщения.
    """
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено")

    text = stt.audio_to_text(file_on_disk)
    if not text:
        text = "Формат документа не поддерживается"
    await message.answer(text)

    os.remove(file_on_disk)  # Удаление временного файла


if __name__ == "__main__":
    # Запуск бота
    print("Запуск бота")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass