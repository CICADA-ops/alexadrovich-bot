from PIL import Image


def convert(im_path, c_from, c_to):
    if c_from == 'png':
        img = Image.open(im_path)
        img = img.convert('RGB')
        img.save(f'{im_path.replace(c_from, '')}{c_to}')
    else:
        img = Image.open(im_path)
        img.save(f'{im_path.replace(c_from, '')}{c_to}')


im_path = 'Photo.jpg'