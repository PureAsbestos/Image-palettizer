import palettizer
import loadgpl
from imageio import imread, imwrite
import numpy as np
from time import time

palette_name = input('Where is the palette?\n\n')
palette = loadgpl.load_rgb(palette_name)
image = imread(input('\nWhere is the image?\n\n'))

t0 = time()

if image.shape[0] * image.shape[1] < 1024:
    imwrite('output.png', palettizer.palettize(palette, image))
else:
    image_sliced = np.array_split(image, image.shape[0] * image.shape[1] // 1024)
    print('\nImage will be split into ' + str(len(image_sliced)) + ' pieces.\n')
    print('Processing...')
    image_output_sliced = [
    palettizer.palettize(palette, image_sec)
    for image_sec in image_sliced
    ]
    image_output = np.concatenate(image_output_sliced)

    imwrite('output.png', image_output)

print('\nDone!\n')

t1 = time()

deltaT = t1 - t0

print('Finished in ' + str(deltaT) + ' seconds.\n')
