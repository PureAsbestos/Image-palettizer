import palettizer
import loadgpl
from imageio import imread, imwrite
import numpy as np
from time import time
from dithermaps import *
from tempfile import TemporaryFile
from tqdm import tqdm
import qprompt as qp
import os

qp.title("Image Palettizer")

valid_path = lambda x: os.path.exists(x)

palette_name = qp.ask_str("Palette location (must be .gpl file)", valid=valid_path)
qp.clear()
palette = loadgpl.load_rgb(palette_name)

image = imread(qp.ask_str("Image location", valid=valid_path))
qp.clear()

# Load image into temporary .npy file
image_shape = image.shape
file = TemporaryFile()
np.save(file, image)
del image
image = np.memmap(file, mode='w+', offset=128, shape=image_shape)
del image_shape

# For if image is grayscale
if len(image.shape) == 2:
    image = image[..., np.newaxis].repeat(3, axis=2)

if qp.ask_yesno('Use dithering', default='y'):
    qp.clear()
    menu = qp.enum_menu(('ordered', 'diffusion'))
    if menu.show(header='Ordered or diffusion?', default='2') == '2':
        qp.clear()
        use_ordered = False
        menu = qp.enum_menu(DIFFUSION_MAPS.keys())
        dither_type = menu.show(header='Diffusion method?', default='1', returns='desc')
        qp.clear()
        dither_matrix = DIFFUSION_MAPS[dither_type]
    elif qp.ask_yesno('Use image for the map', default='n'):
        qp.clear()
        use_ordered = True
        img_map = imread(qp.ask_str("Image location", valid=valid_path))
        dither_matrix = img_map / 255 if len(img_map.shape) == 2 else img_map[..., 0] / 255
    else:
        qp.clear()
        use_ordered = True
        menu = qp.Menu()
        for key in BAYER_PRECALC.keys():
            menu.add(key, '')
        bayer_size = menu.show(header='Using Bayer. Matrix size?')
        qp.clear()
        dither_matrix = get_bayer_matrix(bayer_size)
else:
    # Default values if something breaks in the menu
    use_ordered = False
    dither_type = None
    dither_matrix = None

t0 = time()

print('Processing...')
imwrite('output/output-' + str(t0) + '.png', palettizer.palettize(palette, image, dither_matrix, use_ordered))
qp.clear()

print('\nDone!\n')

t1 = time()

deltaT = t1 - t0

print('Finished in ' + str(deltaT) + ' seconds.\n')

qp.pause()
