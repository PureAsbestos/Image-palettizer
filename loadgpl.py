import numpy as np

def load_rgb(palette_loc, header_size=3):
    palette_raw = open(palette_loc)  # Open the palette file.
    palette_lines = palette_raw.readlines()  # Read each line of the file.
    palette_raw.close()  # Close the file because we don't need it anymore.
    palette_list = []  # Initialize a list to hold the values later.

    for line in palette_lines[header_size:]:  # Iterate over the each line.
        if not line.startswith('#'):  # Ignore comments.
            color_val = line.split()[:3]  # Split and slice each line.
            palette_list.append(color_val)

    # Convert list of lists to numpy ndarray.
    palette = np.array(palette_list)
    palette = palette.astype(np.uint8)

    return palette
