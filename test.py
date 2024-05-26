'''
import os
import re
import ssl

from docx2pdf import convert
from pdf2docx import Converter

from pytube import *

ssl._create_default_https_context = ssl._create_unverified_context

youtube_object = YouTube('https://youtu.be/j1w5-jF3X9k?si=Ye00Ce4_DHeEpyqZ')

streams = youtube_object.streams
l = set()

for stream in streams:
    if stream.resolution:
        l.add(stream.resolution)
l = sorted(l)
for i in l:
    print(i)
'''
'''
desired_resolution = '144p'
filtered_streams = streams.filter(res=desired_resolution)
stream = filtered_streams.first()
stream.download()
'''

'''
path = 'Photo.jpg'
format_from = '.' + path.split('.')[-1] # .jpg
print(format_from)
format_in = '.png'

print(f'{path.replace(format_from, '')}1{format_in}') # Photo1.png

video_title = 'a/a:a*a?a"a<a>a|a+a'
video_title = re.sub('[/:*?"<>|+]', '', video_title)
print(video_title)

convert('Техническое_задание.docx', 'Техническое_задание1.pdf')
cv = Converter('Техническое_задание1.pdf')
cv.convert('Техническое_задание2.docx')
cv.close()
'''
'''
144p
240p
360p
480p
720p
'''
import ssl
from pytube import YouTube

ssl._create_default_https_context = ssl._create_unverified_context

resolution = '720p'
youtube_link = 'https://youtu.be/tN13gRqAfss?si=_ns47uEOR_L7dWmF'

youtube_object = YouTube(youtube_link)
streams = youtube_object.streams
filtered_streams = streams.filter(res=resolution)
stream = filtered_streams.first()


print(stream.on_progress)
