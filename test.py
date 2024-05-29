from pytube import *

import ssl

import mimetypes

ssl._create_default_https_context = ssl._create_unverified_context

youtube_link = 'https://youtu.be/lTo6aG7xD6I?si=edcomtuTJpZgAPQB'
youtube_object = YouTube(youtube_link)
streams = youtube_object.streams
stream = streams.get_highest_resolution()

print(stream.default_filename)


url = f'http://127.0.0.1:8081/bot{bot_token}/sendDocument'

mime_type, _ = mimetypes.guess_type(new_img)

payload = {'chat_id': callback.message.chat.id,
           'supports_streaming': 'true'}

files = [
    ('document', (new_img, open(new_img, 'rb'), mime_type))
]

response = requests.post(url, data=payload, files=files)
print(response.text)

