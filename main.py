import palettizer
import loadgpl
import lospec
from imageio import imread, imwrite
import numpy as np
from dithermaps import *
from tempfile import TemporaryFile, NamedTemporaryFile
import PySimpleGUI as sg
from sg_extensions import error_popup
import os, sys, io
from PIL import Image, ImageTk
import multiprocess as multi
import multipatch

from constants import VERSION, DATA_LOC, EXT_LIST

icon_loc = str(os.path.join(DATA_LOC, 'icon.ico'))
sg.SetOptions(button_color=('black','#DDDDDD'), icon=icon_loc)

if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

if sys.platform == 'darwin':
    lospec.BTN_TXT_C = '#000'


def do_palettize(palette, image, *args, **kwargs):

    # For if image is grayscale
    if len(image.shape) == 2:
        image = image[..., np.newaxis].repeat(3, axis=2)

    return palettizer.palettize(palette, image, *args, **kwargs)


THUMBNAIL_SIZE = (610, 610)
def image_popup(image):
    temp_img = Image.fromarray(image)
    w, h = temp_img.size

    if w > THUMBNAIL_SIZE[0] or h > THUMBNAIL_SIZE[1]:
        temp_img.thumbnail(THUMBNAIL_SIZE, Image.LANCZOS)
    else:
        ratio = min(THUMBNAIL_SIZE[0] / w, THUMBNAIL_SIZE[1] / h)
        temp_img = temp_img.resize((int(w * ratio), int(h * ratio)), Image.NEAREST)

    with io.BytesIO() as im_bytes:
        temp_img.save(im_bytes, format="GIF")
        im_bytes = im_bytes.getvalue()

    layout = [[sg.Image(data=im_bytes, size=THUMBNAIL_SIZE)],
              [sg.Text('Save location', justification='right'), sg.InputText(do_not_clear=True, key='file'), sg.SaveAs()],
              [sg.Save(), sg.Cancel()]]

    window = sg.Window('Output Image', auto_size_text=True).Layout(layout).grab_set()
    while True:
        event, values = window.Read()
        if event == 'Save':
            writefile = values['file']
            try:
                if '.' in writefile and writefile.split('.')[-1] in EXT_LIST:
                    imwrite(writefile, image)
                else:
                    imwrite(writefile + '.png', image)
                break
            except Exception as e:
                error_popup(e, 'Error saving image: ')
        else:
            break
    window.grab_release().Close()


################################################################################
# TODO: Commentary

if __name__ == '__main__':
    # Necessary for Windows bundles
    multi.freeze_support()

    no_dither_radio = sg.Radio('None', 'RADIO1', enable_events=True, default=True, key='none radio')
    ordered_radio = sg.Radio('Ordered', 'RADIO1', enable_events=True, key='ordered radio')
    diffusion_radio = sg.Radio('Diffusion', 'RADIO1', enable_events=True, key='diffusion radio')
    ordered_combo = sg.Combo(list(BAYER_PRECALC.keys()), readonly=True, disabled=True, key='ordered combo')
    diffusion_combo = sg.Combo(list(DIFFUSION_MAPS.keys()), readonly=True, disabled=True, key='diffusion combo')
    bleed_spin = sg.Spin(list(np.arange(101)/100), initial_value=1.0, key='bleed')

    frame_dithering_layout = [[sg.Text('')],
                              [sg.Column([[no_dither_radio], []]), sg.Column([[ordered_radio], [ordered_combo]]),
                               sg.Column([[diffusion_radio], [diffusion_combo]]), sg.Column([[sg.Text('Bleed')], [bleed_spin]])],
                              [sg.Text('')]]
    frame_dithering = sg.Frame('Dithering', frame_dithering_layout, pad=(0, 10))

    layout = [[sg.Text('', size=(49, 1)), sg.Button('Get palette from Lospec', pad=(0, 20), enable_events=True, key='lospec')],
              [sg.Text('GPL palette', size=(15, 1), justification='right'), sg.InputText(do_not_clear=True, key='palette'), sg.FileBrowse()],
              [sg.Text('Image', size=(15, 1), justification='right'), sg.InputText(do_not_clear=True, key='image'), sg.FileBrowse()],
              [sg.Text('')],
              [sg.Text('', size=(5, 1)), frame_dithering],
              [sg.Button('Apply', pad=(5, 20), bind_return_key=True)]]

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

        if event == 'lospec':
            try:
                window.FindElement('palette').Update(lospec.palette_retriever())
            except Exception as e:
                error_popup(e)

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
                    try:
                        image_popup(output_image)
                    except Exception as e:
                        error_popup(e)

    window.Close()
