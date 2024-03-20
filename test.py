import os
import re

'''
path = 'Photo.jpg'
format_from = '.' + path.split('.')[-1] # .jpg
print(format_from)
format_in = '.png'

print(f'{path.replace(format_from, '')}1{format_in}') # Photo1.png
'''

video_title = 'a/a:a*a?a"a<a>a|a+a'
video_title = re.sub('[/:*?"<>|+]', '', video_title)
print(video_title)