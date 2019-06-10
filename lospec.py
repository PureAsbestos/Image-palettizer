import os
import webbrowser
import PySimpleGUI as sg
import requests
from main import error_popup

layout = [[sg.Text('Browse palettes on Lospec', text_color='blue', font=('default', 12, 'underline'), tooltip='https://lospec.com/palette-list', enable_events=True, key='link')],
          [sg.Text('Name of palette on Lospec', size=(22, 1), justification='right'), sg.InputText(do_not_clear=True, key='palette'), sg.Button('Get', bind_return_key=True)]]


def palette_retriever():
    window = sg.Window('Lospec Palette Retriever', auto_size_text=True).Layout(layout)

    while True:
        event, values = window.Read()
        if event is None:
            break
        elif event == 'link':
            webbrowser.open('https://lospec.com/palette-list')
        elif event == 'Get':
            try:
                palette_name = '-'.join(values['palette'].casefold().strip().split())
                r = requests.get(f'https://lospec.com/palette-list/{palette_name}.gpl', timeout=1)
                r.raise_for_status()
                if not os.path.exists('./palettes'):
                    os.mkdir('./palettes')
                with open(f'./palettes/{palette_name}.gpl', mode='wb+') as f:
                    f.write(r.content)
                window.Close()
                return f'./palettes/{palette_name}.gpl'
            except Exception as e:
                error_popup(e, 'Could not retrieve palette: ')

    window.Close()
