from PIL import Image


def convert_any(im_path, c_from, c_to):
    if c_from == 'png':
        img = Image.open(im_path)
        img = img.convert('RGB')
        img.save(f'{im_path.replace(c_from, '')}{c_to}')
    else:
        img = Image.open(im_path)
        img.save(f'{im_path.replace(c_from, '')}{c_to}')


im_path = input('Точный путь к файлу ')
c_from = im_path.split('.')[-1]
c_to = input('В какой формат нужно переформатировать? ')

convert_any(im_path, c_from, c_to)
