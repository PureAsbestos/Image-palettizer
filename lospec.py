import os
import re
import webbrowser
import PySimpleGUI as sg
from sg_extensions import error_popup
import requests
from constants import DATA_LOC

BG_C = '#332f35'
TXT_C = '#b3adb6'
BTN_C = '#4d4750'
BTN_TXT_C = '#fff'
BOX_C = '#29252a'

layout = [[sg.Image(os.path.join(DATA_LOC, 'lospec.gif'), pad=((180, 0), (120, 105)), size=(332, 80), tooltip='https://lospec.com/palette-list', background_color=BG_C, enable_events=True, key='link')],
          [sg.Text('Name of palette on Lospec:', size=(22, 1), justification='right', text_color=TXT_C, background_color=BG_C),
           sg.InputText(do_not_clear=True, background_color=BOX_C, text_color=BTN_TXT_C, key='palette'), sg.Button('Get', button_color=(BTN_TXT_C, BTN_C), bind_return_key=True, pad=(10, 0))],
           [sg.Text('', background_color=BG_C)]]


def palette_retriever():
    window = sg.Window('Lospec Palette Retriever', background_color=BG_C, font=('Arial', 0, ''), auto_size_text=True).Layout(layout).grab_set()
    while True:
        event, values = window.Read()
        if event is None:
            break
        elif event == 'link':
            webbrowser.open('https://lospec.com/palette-list')
        elif event == 'Get':
            try:
                palette_name = '-'.join(re.sub(r'([^\w\s-]|[_])', '', values['palette'].casefold().strip()).split())
                r = requests.get(f'https://lospec.com/palette-list/{palette_name}.gpl', timeout=1.5)
                r.raise_for_status()
                if not os.path.exists('./palettes'):
                    os.mkdir('./palettes')
                pal_path = os.path.abspath(f'./palettes/{palette_name}.gpl')
                with open(pal_path, mode='wb+') as f:
                    f.write(r.content)
                window.Close()
                return pal_path
            except Exception as e:
                window.grab_release()
                error_popup(e, 'Could not retrieve palette: ')
                window.grab_set()

    window.Close()
