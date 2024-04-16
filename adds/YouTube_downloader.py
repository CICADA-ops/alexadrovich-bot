import ssl

from pytube import *
import moviepy
from moviepy.editor import *
import os

ssl._create_default_https_context = ssl._create_unverified_context


def download_video(link):
    youtubeObject = YouTube(link)
    #youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


def download_audio(link):
    try:
        youtubeObject = YouTube(link)
        audio_stream = youtubeObject.streams.get_audio_only()

        name = f"{audio_stream.title}.mp3".replace("/", "-").replace("|", "-")
        audio_stream.download(filename=name)
        print("Audio download is completed successfully.")
    except Exception as e:
        print(f"An error has occurred: {e}")


link = input("Отправьте ссылку на YouTube видео: ")
choice = input("Вы хотите скачать видео или аудио? Введите 'видео' или 'аудио': ").lower()

if choice == "видео":
    download_video(link)
elif choice == "аудио":
    download_audio(link)
else:
    print("Неверный выбор. Пожалуйста, выберите 'видео' или 'аудио'.")
