from pytube import *

import ssl
import os
import mimetypes

ssl._create_default_https_context = ssl._create_unverified_context
'''
youtube_link = 'https://youtu.be/lTo6aG7xD6I?si=edcomtuTJpZgAPQB'
youtube_object = YouTube(youtube_link)
audio_part = youtube_object.streams.get_audio_only()
streams = youtube_object.streams
filtered_streams = streams.filter(res='720p')
stream = filtered_streams.first()
mime_type = stream.mime_type

video_title = stream.default_filename
audio_title = audio_part.default_filename

print(video_title)
print(audio_title)
'''
video_title = 'НЕИГРЫ  Варя Щербакова VS Оля Парфенюк.webm'
cmd = f'ffmpeg -i "{video_title}" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k "1_{video_title.split('.')[0]}.mp4"'
os.system(cmd)

