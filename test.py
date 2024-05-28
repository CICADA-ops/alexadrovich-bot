from pytube import *

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

youtube_link = 'https://youtu.be/lTo6aG7xD6I?si=edcomtuTJpZgAPQB'
youtube_object = YouTube(youtube_link)
streams = youtube_object.streams
stream = streams.get_highest_resolution()

print(stream.default_filename)
