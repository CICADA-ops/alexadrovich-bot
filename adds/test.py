from pytube import *

import ssl
import os
import mimetypes

ssl._create_default_https_context = ssl._create_unverified_context

youtube_link = 'https://youtu.be/HRbW75fYLvo?si=z_jI4H7Re_hCQXvu'
youtube_object = YouTube(youtube_link)
streams = youtube_object.streams
stream = streams.filter(res='720p').first()
print(stream.filesize_mb / 1024)
stream = streams.filter(res='480p').first()
print(stream.filesize_mb / 1024)
