import palettizer
import loadgpl
from imageio import imread, imwrite
import numpy as np
from dithermaps import *
from tempfile import TemporaryFile, NamedTemporaryFile
import PySimpleGUI as sg
import os, sys

VERSION = 'v2.1.0'
sg.SetOptions(button_color=('black','#DDDDDD'))

EXT_LIST = ['tif', 'tiff', 'stk', 'lsm', 'bmp', 'ps', 'eps', 'gif',
            'ico', 'im', 'jfif', 'jpe', 'jpg', 'jpeg', 'mpo', 'pcx',
            'png', 'pbm', 'pgm', 'ppm', 'bw', 'rgb', 'rgba', 'sgi',
            'tga', 'bsdf', 'npz']

if 'win' in sys.platform:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


def error_popup(e, prefix='Error: '):
    sg.PopupOK(prefix + str(e), title='ERROR', text_color='red')


def do_palettize(palette, image, *args, **kwargs):

    # For if image is grayscale
    if len(image.shape) == 2:
        image = image[..., np.newaxis].repeat(3, axis=2)

    return palettizer.palettize(palette, image, *args, **kwargs)


shuffle = np.random.RandomState(seed=42).permutation
def get_div_points(a, b):
        Neach_section, extras = divmod(a, b)
        section_sizes = shuffle(extras * [Neach_section + 1] +
                                (b - extras) * [Neach_section])
        return np.array(section_sizes, dtype=np.intp).cumsum()


def resize_img(image, side_length):
    h, w = image.shape[:2]
    max_wh = max(w, h)

    if h > w:
        height = side_length
        width = int(w * side_length / h)
    else:
        width = side_length
        height = int(h * side_length / w)

    if side_length > max_wh:
        reps = max(width, height) // max_wh
        img = np.repeat(image, reps, axis=1)  # X
        img = np.repeat(img, reps, axis=0)  # Y
    elif side_length == max_wh:
        img = image
    else:
        arr = np.array_split(image, get_div_points(w, width), axis=1)  # X
        arr = [np.mean(chunk, axis=1, keepdims=True) for chunk in arr]  # X
        arr = np.concatenate(arr, axis=1)  # X

        arr = np.array_split(arr, get_div_points(h, height), axis=0)  # Y
        arr = [np.mean(chunk, axis=0, keepdims=True) for chunk in arr]  # Y
        img = np.concatenate(arr, axis=0).astype(np.uint8)  # Y

    return img


def image_popup(image):
    temp_img = resize_img(image, 512)
    temp = NamedTemporaryFile(suffix='.gif', mode='wb', delete=False)
    temp_name = temp.name
    imwrite(temp, temp_img, format='gif')
    layout = [[sg.Image(filename=temp_name, size=(512,512))],
              [sg.Text('Save location', justification='right'), sg.InputText(do_not_clear=True, key='file'), sg.SaveAs()],
              [sg.Save(), sg.Cancel()]]

    window = sg.Window('Output Image', auto_size_text=True).Layout(layout)
    while True:
        event, values = window.Read()
        if event == 'Save':
            try:
                if '.' in values['file'] and values['file'].split('.')[-1] in EXT_LIST:
                    imwrite(values['file'], image)
                else:
                    imwrite(values['file'] + '.png', image)
                break
            except Exception as e:
                sg.PopupOK('Error saving image: ' + str(e), title='ERROR', text_color='red')
        else:
            break
    window.Close()
    temp.close()
    os.remove(temp_name)


################################################################################
# TODO: Commentary

no_dither_radio = sg.Radio('None', 'RADIO1', enable_events=True, default=True, key='none radio')
ordered_radio = sg.Radio('Ordered', 'RADIO1', enable_events=True, key='ordered radio')
diffusion_radio = sg.Radio('Diffusion', 'RADIO1', enable_events=True, key='diffusion radio')
ordered_combo = sg.Combo(list(BAYER_PRECALC.keys()), readonly=True, disabled=True, key='ordered combo')
diffusion_combo = sg.Combo(list(DIFFUSION_MAPS.keys()), readonly=True, disabled=True, key='diffusion combo')
bleed_spin = sg.Spin(list(np.arange(101)/100), initial_value=1.0, key='bleed')

layout = [[sg.Text('GPL palette', size=(15, 1), justification='right'), sg.InputText(do_not_clear=True, key='palette'), sg.FileBrowse()],
          [sg.Text('Image', size=(15, 1), justification='right'), sg.InputText(do_not_clear=True, key='image'), sg.FileBrowse()],
          [sg.Text('Dithering')],
          [sg.Column([[no_dither_radio], []]), sg.Column([[ordered_radio], [ordered_combo]]),
           sg.Column([[diffusion_radio], [diffusion_combo]]), sg.Column([[sg.Text('Bleed')], [bleed_spin]])],
          [sg.Button('Apply', enable_events=True)]]

window = sg.Window('Image Palettizer ' + VERSION, auto_size_text=True).Layout(layout)

# Event loop
while True:
    event, values = window.Read()

    if event is None:
        break

    if values['ordered radio']:
        window.FindElement('ordered combo').Update(disabled=False)
    else:
        window.FindElement('ordered combo').Update(disabled=True)

    if values['diffusion radio']:
        window.FindElement('diffusion combo').Update(disabled=False)
    else:
        window.FindElement('diffusion combo').Update(disabled=True)

    if values['none radio']:
        window.FindElement('bleed').Update(disabled=True)
    else:
        window.FindElement('bleed').Update(disabled=False)

    if event == 'Apply':
        palette_loc = values['palette']
        image_loc = values['image']
        use_ordered = values['ordered radio']

        if not values['none radio']:
            try:
                bleed = float(values['bleed'])
                assert (-1e100 <= bleed <= 1e100), 'Value must be between -1e100 and 1e100'
            except Exception as e:
                error_popup(e, 'Error in bleed value: ')
                bleed = None
                palette = None
                image = None

        if use_ordered:
            dither_matrix = get_bayer_matrix(values['ordered combo'])
        elif values['diffusion radio']:
            dither_matrix = DIFFUSION_MAPS[values['diffusion combo']]
        else:
            dither_matrix = None
            bleed = None

        try:
            palette = loadgpl.load_rgb(palette_loc)
        except Exception as e:
            error_popup(e, 'Error loading palette: ')
            palette = None

        try:
            image = imread(image_loc)
        except Exception as e:
            error_popup(e, 'Error loading image: ')
            image = None

        if (palette is not None) and (image is not None):
            try:
                output_image = do_palettize(palette, image, dither_matrix, use_ordered, bleed)
            except Exception as e:
                error_popup(e, 'Error during palettization: ')
                image = None
            else:
                image_popup(output_image)

window.Close()
