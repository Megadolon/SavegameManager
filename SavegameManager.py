import PySimpleGUI as sg
import keyboard
from SavegameHandlerClass import SavegameHandler
import pygame
import json


my_theme = {
    'BACKGROUND': '#282c34',
    'TEXT': '#ffffff',
    'INPUT': '#c7cbd1',
    'TEXT_INPUT': '#282c34',
    'SCROLL': '#c7cbd1',
    'BUTTON': ('#282c34', '#ffffff'),
    'PROGRESS': ('#01826B', '#D0D0D0'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
    'RELIEF': 'groove'  # add the relief element to the theme
}
with open('my_theme.json', 'w') as file:
    json.dump(my_theme, file)

sg.theme_add_new('my_theme', my_theme)
sg.theme('my_theme')

#hexvalues
color_background_light = '#FFFFFF'
color_boxes_light = '#969696'
color_button_light = '#E1E1E1'
color_text_light = '#000000'

color_background_dark = '#222222'
color_boxes_dark = '#696969'
color_button_dark = '#1E3973'
color_text_dark = '#FFFFFF'

color_background = color_background_dark
color_boxes = color_boxes_dark
color_button = color_button_dark
color_text = color_text_dark

icon_path = 'res//images//SavegameManager.ico'
textFont = ("Arial", 11)

settings_volume = int(100)

isRunning=False

audio_save = "res//audio//save.wav"
audio_load = "res//audio//load.wav"


pygame.init()

def play_audio(audio):
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()

def on_press_f9(event):
    if not isRunning:
        return
    if event.name == 'f9':
        global handler
        handler.load_data()
        if sound:
            play_audio(audio_load)

def on_press_f5(event):
    if not isRunning:
        return
    if event.name == 'f5':
        global handler
        handler.save_data()
        if sound:
            play_audio(audio_save)

# Define your function that will be called when the button is pressed
def selectsavegame_callback():
    # Open the folder browser dialog and get the selected folder path
    folder_path = sg.popup_get_folder("Select a savegame folder", default_path=window['-OUTPUT-'].get(), size=(80, 1), font=textFont, button_color=(color_text, color_button), background_color=color_boxes, icon=icon_path)

    # Update the text of the output element to display the selected folder path
    if folder_path:
        window["-OUTPUT-"].update(f"{folder_path}")

def selectbackup_callback():
    # Open the folder browser dialog and get the selected folder path
    folder_path = sg.popup_get_folder("Select a backup folder", default_path=window['-OUTPUT-2'].get(), size=(80, 1), font=textFont, button_color=(color_text, color_button), background_color=color_boxes, icon=icon_path)

    # Update the text of the output element to display the selected folder path
    if folder_path:
        window["-OUTPUT-2"].update(f"{folder_path}")

def dark_mode_toggle(toggle_value, window_settings):
    global color_background
    global color_boxes
    global color_button
    global color_text

    if toggle_value:
        color_background = color_background_dark
        color_boxes = color_boxes_dark
        color_button = color_button_dark
        color_text = color_text_dark
    else:
        color_background = color_background_light
        color_boxes = color_boxes_light
        color_button = color_button_light
        color_text = color_text_light
    
    for element in window.element_list() + window_settings.element_list():
        if isinstance(element, sg.Button):
            element.update(button_color=(color_text, color_button))
        if isinstance(element, sg.Text):
            element.update(text_color=color_text)
            element.update(background_color=color_background)
        if isinstance(element, sg.Checkbox):
            element.update(background_color=color_button)
            element.update(text_color=color_text)
            element.update(checkbox_color=color_boxes)
        #if isinstance(element, sg.Frame):
            #element.TKroot.configure(background=color0)

    window.TKroot.configure(background=color_background)
    window.Refresh()

# Define the layout of your GUI window
layout = [
    [sg.Frame("Savegame Location", [
        [sg.Button("Select folder", key="-BUTTON-", size=(10,1), font=textFont),
         sg.Text("no path", size=(80,1), text_color=color_text,  key="-OUTPUT-", background_color=color_background, font=textFont)]
    ], border_width=1, relief="flat", background_color=color_boxes, key="-FRAME-")],
    [sg.Frame("Backup Location", [
        [sg.Button("Select folder", key="-BUTTON-2", size=(10,1), font=textFont),
         sg.Text("no path", size=(80,1), text_color=color_text, key="-OUTPUT-2", background_color=color_background, font=textFont)]
    ], border_width=1, relief="flat", background_color=color_boxes)],

    [sg.Frame("", [
        [sg.Button("Start", key="-BUTTON-START", size=(10,1), font=textFont),
         sg.Button("Stop", key="-BUTTON-STOP", size=(10,1), disabled=True, font=textFont),
         sg.Button("Settings", key="-BUTTON_SETTINGS-", size=(10,1), disabled=False, font=textFont)]
         
    ], border_width=1, relief="flat", background_color=color_boxes)]

]

def custom_print(*args, **kwargs):
    # Convert arguments to a string
    message = " ".join(map(str, args))
    
    # Append the message to the output element
    window['-OUTPUT_CONSOLE-'].print(message, **kwargs)


def popup_window(message):
    column_to_be_centered = [
                             [sg.Text(message, text_color=color_text, background_color=color_boxes, font=textFont)],
                             [sg.Button('Ok!', size=(150, 75), font=textFont)],
                            ]

    layoutConfigValid = [
                         [sg.VPush(background_color=color_boxes)],
                         [sg.Push(background_color=color_boxes), sg.Column(column_to_be_centered, element_justification='c', background_color=color_boxes), sg.Push()],
                         [sg.VPush(background_color=color_boxes)]
                        ]
    windowConfigValid = sg.Window(message, layoutConfigValid, background_color=color_boxes, button_color=(color_text, color_button), size=(350,100), finalize=True, keep_on_top=True, modal=True)
    windowConfigValid.set_icon(icon_path)
    event, values = windowConfigValid.read(close=True)

sound = True
    

# Create the window using the layout
window = sg.Window("Savegame Manager", layout, background_color=color_background, finalize=True, button_color=(color_text, color_button), theme=my_theme)
window.set_icon(icon_path)
window.set_min_size((875, 175))

handler = SavegameHandler()
handler.load_config()

def open_settings_menu():

    global sound
    global settings_volume
    print("settings opened: " + str(sound))

    layout_settings =   [
                            [sg.Checkbox("Sound", key="-SOUND-", size=(10,1), default=sound, checkbox_color=color_boxes, background_color=color_button, enable_events=True, font=textFont, metadata=True)],
                            [sg.Slider(range=(0, 100), orientation='horizontal', size=(20, 15), default_value=50, resolution=1, enable_events=True, key='-SLIDER-')],
                            [sg.Checkbox("Dark Mode", key="-TOGGLE-", size=(10,1), default=True, checkbox_color=color_boxes, background_color=color_button, enable_events=True, font=textFont, metadata=True)],
                            [sg.Button('Submit'), sg.Button('Cancel')]
                        ]
                        
    window_settings = sg.Window("Settings", layout_settings, background_color=color_boxes, button_color=(color_text, color_button), size=(350,200), finalize=True, keep_on_top=True, modal=True)
    window_settings.set_icon(icon_path)

    while True:

        event, values = window_settings.read()

        if event == "-SOUND-":
             sound = values["-SOUND-"]
             print("sound checkbox pressed: " + str(sound))

        if event == '-SLIDER-':
            settings_volume = values["-SLIDER-"]
        
        if event == "-TOGGLE-":
            dark_mode_toggle(values['-TOGGLE-'], window_settings)

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

    print("settings closed: " + str(sound))
    window_settings.close()

if not handler.config_valid():
    popup_window('invalid paths')
else:
    window["-OUTPUT-"].update(handler.src_path)
    window["-OUTPUT-2"].update(handler.dest_path)


keyboard.on_release(on_press_f5)
keyboard.on_release(on_press_f9)
# Start the event loop to process events and wait for user interaction
while True:

    event, values = window.read()

    # If the user closes the window or clicks the Exit button, exit the event loop
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    # If the user clicks the button, call the button_callback function
    if event == "-BUTTON-":
        selectsavegame_callback()

    if event == "-BUTTON-2":
        selectbackup_callback()

    if event == "-BUTTON_SETTINGS-":
        open_settings_menu()

    if event == "-BUTTON-START":
        handler.set_config(window['-OUTPUT-'].get(), window['-OUTPUT-2'].get())
        is_valid, error_msg = handler.config_valid()
        if is_valid:
            window["-BUTTON-"].update(disabled=True)
            window["-BUTTON-2"].update(disabled=True)
            window["-BUTTON-STOP"].update(disabled=False)
            window["-BUTTON-START"].update(disabled=True)
            isRunning = True
        else:
            popup_window(error_msg)
    
    if event == "-BUTTON-STOP":
        window["-BUTTON-"].update(disabled=False)
        window["-BUTTON-2"].update(disabled=False)
        window["-BUTTON-START"].update(disabled=False)
        window["-BUTTON-STOP"].update(disabled=True)
        isRunning=False


# Close the window and exit the program
is_valid, error_msg = handler.config_valid()
if is_valid:
    handler.save_config()
    
window.close()