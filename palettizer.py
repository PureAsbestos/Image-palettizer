import numpy as np
from colorspacious import deltaE


def palettize(palette_array, image_array):

    palette = palette_array

    image_input = image_array

    # Palettize image.
    distances_1 = np.repeat(image_input[..., 0, np.newaxis], palette.shape[0], axis=2)
    distances_2 = np.repeat(image_input[..., 1, np.newaxis], palette.shape[0], axis=2)
    distances_3 = np.repeat(image_input[..., 2, np.newaxis], palette.shape[0], axis=2)

    distances = np.stack((distances_1, distances_2, distances_3), axis=3)

    distances = deltaE(distances, palette, 'sRGB255')

    image_output = distances.argmin(axis=2)

    image_output = np.repeat(image_output[:, :, np.newaxis], 3, axis=2)

    image_output[:, :, 0] = palette[image_output[:, :, 0], 0]
    image_output[:, :, 1] = palette[image_output[:, :, 1], 1]
    image_output[:, :, 2] = palette[image_output[:, :, 2], 2]

    return image_output
