import numpy as np
from colorspacious import deltaE
from dithermaps import DIFFUSION_MAPS, get_bayer_matrix
from constants import DATA_LOC
import PySimpleGUI as sg
import sg_extensions
from psutil import virtual_memory
import multiprocess as multi
import os


def index2rgb(arr, pal):
    channels = [pal[arr, i] for i in range(3)]
    out = np.stack(channels, axis=-1)
    return out


def counter(iterable, message='', id='single', end=None):
    end = len(iterable) if end is None else end
    sg.OneLineProgressMeter(message, 0, end, id)
    for i, val in enumerate(iterable):
        yield val
        if not sg.OneLineProgressMeter(message, i+1, end, id):
            break


def split_deltaE(image, color2, *args, **kwargs):
    split_val = 25000 * np.ceil(virtual_memory()[1] / 1024**3)
    splits = np.ceil((len(color2)**0.5555) * image.shape[0] * image.shape[1] / split_val)
    image_sliced = np.array_split(image, splits)
    pool = multi.Pool(processes=min([multi.cpu_count(), splits]))
    image_output_sliced = pool.imap(lambda x: deltaE(x, color2, *args, **kwargs), image_sliced)
    image_output_sliced = [a for a in counter(image_output_sliced, 'Quantizing...', end=splits)]
    pool.close()
    return np.concatenate(image_output_sliced)


def palettize(palette, image_input, dither_matrix=None, use_ordered=False, bleed=1.0):
    # Repeat each channel of the image to the length of the palette
    distances_1 = np.repeat(image_input[..., 0, np.newaxis], palette.shape[0], axis=2)
    distances_2 = np.repeat(image_input[..., 1, np.newaxis], palette.shape[0], axis=2)
    distances_3 = np.repeat(image_input[..., 2, np.newaxis], palette.shape[0], axis=2)

    # Combine channels
    distances = np.stack((distances_1, distances_2, distances_3), axis=3)
    del distances_1, distances_2, distances_3

    # Find the distance between each pixel color and every palette color
    distances = split_deltaE(distances, palette, 'sRGB255')

    # Find the closest palette color
    image_quantized = np.array(distances.argmin(axis=2))

    # Dithering
    if (not use_ordered) and (dither_matrix is not None):
        quant_error = distances.min(axis=2)
        for row in range(distances.shape[0]):
            if not sg.OneLineProgressMeter('Dithering...', row+1, distances.shape[0], 'single'):
                break
            for col in range(distances.shape[1]):
                quant_error[row, col] = distances[row, col].min()
                image_quantized[row, col] = distances[row, col].argmin()
                pal_index = image_quantized[row, col]
                distances[row, col, pal_index] = 0
                for triple in dither_matrix:
                    try:
                        distances[row + triple[1], col +
                                  triple[0], pal_index] += quant_error[row, col] * triple[2] * bleed
                    except IndexError:
                        pass
        image_indexed = distances.argmin(axis=2)
    elif use_ordered:
        image_quant2 = np.argpartition(distances, 1)[..., 1]  # Get the second closest colors
        image_indexed = np.zeros(distances.shape[:2]).astype('intp')
        for row in range(distances.shape[0]):
            if not sg.OneLineProgressMeter('Dithering...', row+1, distances.shape[0], 'single'):
                break
            for col in range(distances.shape[1]):
                near_color = image_quantized[row, col]
                far_color = image_quant2[row, col]

                colors = sorted([near_color, far_color])
                dists = [distances[row, col, colors[0]], distances[row, col, colors[1]]]

                image_indexed[row, col] = colors[0] if \
                (dists[0] / sum(dists)) + dither_matrix[row % dither_matrix.shape[0], col % dither_matrix.shape[1]] < bleed \
                else colors[1]

    else:  # Type must be no dithering (plain quantization)
        image_indexed = image_quantized
    del image_quantized
    # Indexed to sRGB255
    image_output = index2rgb(image_indexed, palette)
    del image_indexed

    return image_output
