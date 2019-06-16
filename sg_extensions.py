import PySimpleGUI as sg


def grab_set(self):
    self.Finalize()
    self.TKroot.grab_set()
    return self


sg.Window.grab_set = grab_set


def grab_release(self):
    self.Finalize()
    self.TKroot.grab_release()
    return self


sg.Window.grab_release = grab_release


def custom_popup_ok(*args, **kwargs):
    """
    Popup - Display a popup box with as many params as you wish to include
    :param args:
    :param button_color:
    :param background_color:
    :param text_color:
    :param button_type:
    :param icon:
    :param line_width:
    :param font:
    :param no_titlebar:
    :param grab_anywhere:
    :param keep_on_top:
    :param location:
    :param title:
    :return:
    """
    button_color = kwargs.get('button_color')
    text_color = kwargs.pop('text_color', None)
    line_width = kwargs.get('line_width')
    background_color = kwargs.get('background_color')

    if not args:
        args_to_print = ['']
    else:
        args_to_print = args
    if line_width != None:
        local_line_width = line_width
    else:
        local_line_width = sg.MESSAGE_BOX_LINE_WIDTH
    kwargs['title'] = kwargs.get('title', args_to_print[0])
    window = sg.Window(**kwargs)
    max_line_total, total_lines = 0, 0
    for message in args_to_print:
        message = str(message)
        if message.count('\n'):
            message_wrapped = message
        else:
            message_wrapped = sg.textwrap.fill(message, local_line_width)
        message_wrapped_lines = message_wrapped.count('\n') + 1
        longest_line_len = max([len(l) for l in message.split('\n')])
        width_used = min(longest_line_len, local_line_width)
        max_line_total = max(max_line_total, width_used)
        # height = _GetNumLinesNeeded(message, width_used)
        height = message_wrapped_lines
        window.AddRow(
            sg.Text(message_wrapped, auto_size_text=True, text_color=text_color, background_color=background_color))
        total_lines += height


    window.AddRow(sg.CloseButton('OK', size=(5, 1), button_color=button_color, focus=True, bind_return_key=True,
                                  pad=((20, 0), 3)))


    button, values = window.grab_set().Read()

    return button


def error_popup(e, prefix='Error: '):
    custom_popup_ok(prefix + str(e), title='ERROR', text_color='red')
