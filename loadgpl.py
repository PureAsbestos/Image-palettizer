import numpy as np
from time import time
# import functools
# from importlib import import_module

def load_rgb(palette_loc, header_size=0, use_names=False):
    palette_raw = open(palette_loc)  # Open the palette file.
    palette_lines = palette_raw.readlines()  # Read each line of the file.
    palette_raw.close()  # Close the file because we don't need it anymore.
    palette_list = []  # Initialize a list to hold the values later.
    names = []
    if palette_lines[0] != 'GIMP Palette\n':
        raise IOError('Not a GPL file.')
    for line in palette_lines[header_size:]:  # Iterate over the each line.
        if line.strip()[0] in '1234567890':  # Ignore comments.
            color_val = line.split()[:3]  # Split and slice each line.
            if use_names:
                names.append(line.split()[3])
            palette_list.append(color_val)

    # Convert list of lists to numpy ndarray.
    palette = np.array(palette_list)
    palette = palette.astype(np.uint8)

    return ((palette, names) if use_names else palette)


pygame = None
def load_pygame(*args, **kwargs):
    global pygame
    if pygame is None:
        import pygame

    pal = load_rgb(*args, **kwargs)
    return [pygame.Color(*[int(channel) for channel in color]) for color in pal]


def rgb2hex(color):
    return ''.join(format(channel, 'x').rjust(2, '0') for channel in color)


def load_hex(*args, **kwargs):
    pal = load_rgb(*args, **kwargs)
    return np.array(['#' + rgb2hex(color) for color in pal])


def load_int(*args, **kwargs):
    pal = load_rgb(*args, **kwargs)
    return np.array([int(rgb2hex(color), 16) for color in pal])


def write_rgb(location, pal, header={'palette name': '', 'description': ''}, color_names=[]):
    pal = pal.astype(np.uint8)
    lines = []
    if color_names == []:
        color_names = np.full(pal.shape[0], '')
    for triple, name in zip(pal, color_names):
        line = [str(val) + ' ' * (3 - len(str(val))) for val in triple]
        line.append(name)
        line = ' '.join(line)
        lines.append(line)

    header_list = [
        'GIMP Palette', '#Palette name: ' + header['palette name'],
        '#Description: ' + header['description'], '#Colors: ' + str(len(lines))
    ]

    lines = header_list + lines

    f = open(location + header['palette name'] + '_' + str(int(time())) + '.gpl', mode='w+')
    f.write('\n'.join(lines))
    f.close()
