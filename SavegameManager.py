import PySimpleGUI as sg
import keyboard
from SavegameHandlerClass import SavegameHandler
import pygame
import json

class Settings:
    settings_file = 'SavegameManagerSettings.txt'

    def __init__(self):
        self.copy_config = False
        self.sound_enabled = False
        self.sound_volume: int = 0

    @property
    def sound_volume(self):
        return self._sound_volume

    @sound_volume.setter
    def sound_volume(self, value):
        self._sound_volume = max(0, min(value, 100))

def write_settings_to_file(settings):
    with open(settings.settings_file, 'w') as f:
        json.dump(vars(settings), f)

def read_settings_from_file():
    try:
        with open(Settings.settings_file, 'r') as f:
            config = json.load(f)
            settings = Settings()
            for key, value in config.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
            return settings
    except FileNotFoundError:
        return Settings()
    
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

def select_folder_callback(input_field):
    folder_path = sg.popup_get_folder('Select a backup folder', default_path=window[input_field].get(), size=(80, 1))

    if folder_path:
        window[input_field].update(f'{folder_path}')

def popup_window(message):
    column_to_be_centered = [
                             [sg.Text(message)],
                             [sg.Button('Ok!', size=(150, 75))],
                            ]

    layoutConfigValid = [
                         [sg.VPush()],
                         [sg.Push(), sg.Column(column_to_be_centered, element_justification='c'), sg.Push()],
                         [sg.VPush()]
                        ]
    windowConfigValid = sg.Window(message, layoutConfigValid, size=(350,100), finalize=True, keep_on_top=True, modal=True)
    event, values = windowConfigValid.read(close=True)

settings = read_settings_from_file()


icon_path = 'res//images//SavegameManager.ico'
textFont = ('Arial', 5)

my_theme = {
    'BACKGROUND': '#222222',
    'TEXT': '#ffff00',
    'INPUT': '#fff0f0',
    'TEXT_INPUT': '#0000ff',
    'SCROLL': '#00ff00',
    'BUTTON': ('#ff0000', '#00ffff'),
    'PROGRESS': ('#0f0f0f', '#f0f0f0'),
    'BORDER': 10,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
    #'RELIEF': sg.RELIEF_FLAT,
    #'FONT': textFont,
    #'icon': 'res//images//SavegameManager.ico'
}
sg.theme

sg.theme_add_new('my_theme', my_theme)
sg.theme('my_theme')
sg.set_global_icon(icon_path)

settings_volume = int(100)

isRunning=False

audio_save = 'res//audio//save.wav'
audio_load = 'res//audio//load.wav'

pygame.init()


# Define the layout of your GUI window
# Define the layout for the first tab
tab1_manager_layout = [
    [sg.Frame('Savegame Location', [
        [sg.Button('Select folder', key='-BUTTON-SELECT_SAVEGAME_FOLDER', size=(10,1)),
         sg.Text('no path', size=(80,1),  key='-OUTPUT-SAVEGAME_FOLDER')]
    ], border_width=1)],
    [sg.Frame('Backup Location', [
        [sg.Button('Select folder', key='-BUTTON-SELECT_BACKUP_FOLDER', size=(10,1)),
         sg.Text('no path', size=(80,1), key='-OUTPUT-BACKUP_FOLDER')]
    ], border_width=1)],
    [sg.Frame('', [
        [sg.Button('Start', key='-BUTTON-START', size=(10,1)),
         sg.Button('Stop', key='-BUTTON-STOP', size=(10,1), disabled=True)
        ]
    ], border_width=1)]
]

# Define the layout for the second tab
tab2_settings_layout =[
                [sg.Checkbox('Sound', key='-SOUND-', size=(10,1), default=settings.sound_enabled, enable_events=True, metadata=True)],
                [sg.Slider(range=(0, 100), orientation='horizontal', size=(20, 15), default_value=settings.sound_volume, resolution=1, enable_events=True, key='-SLIDER-')],
                [sg.Checkbox('Dark Mode', key='-TOGGLE-', size=(10,1), default=True, enable_events=True, metadata=True)]
            ]

# Define the TabGroup with two tabs
tabgroup_layout = [
    [sg.TabGroup([
        [sg.Tab('Manager', tab1_manager_layout)],
        [sg.Tab('Settings', tab2_settings_layout)]
    ])]
]


sound = True
dark_mode = True

# Create the window using the layout
window = sg.Window('Savegame Manager', tabgroup_layout, finalize=True)
window.set_min_size((875, 175))

handler = SavegameHandler()
handler.load_config()

write_settings =True

if not handler.config_valid():
    popup_window('invalid paths')
else:
    window['-OUTPUT-SAVEGAME_FOLDER'].update(handler.src_path)
    window['-OUTPUT-BACKUP_FOLDER'].update(handler.dest_path)

def run(value: bool):
    window['-BUTTON-SELECT_SAVEGAME_FOLDER'].update(disabled=value)
    window['-BUTTON-SELECT_BACKUP_FOLDER'].update(disabled=value)
    window['-BUTTON-STOP'].update(disabled=not value)
    window['-BUTTON-START'].update(disabled=value)


keyboard.on_release(on_press_f5)
keyboard.on_release(on_press_f9)
# Start the event loop to process events and wait for user interaction
while True:

    event, values = window.read()

    # If the user closes the window or clicks the Exit button, exit the event loop
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # If the user clicks the button, call the button_callback function
    if event == '-BUTTON-SELECT_SAVEGAME_FOLDER':
        select_folder_callback('-OUTPUT-SAVEGAME_FOLDER')

    if event == '-BUTTON-SELECT_BACKUP_FOLDER':
        select_folder_callback('-OUTPUT-BACKUP_FOLDER')

    if event == '-BUTTON-START':
        handler.set_config(window['-OUTPUT-'].get(), window['-OUTPUT-2'].get())
        is_valid, error_msg = handler.config_valid()
        if is_valid:
            run(True)
            isRunning = True
        else:
            popup_window(error_msg)
    
    if event == '-BUTTON-STOP':
        run(False)
        isRunning=False
    
    if event == '-SOUND-':
        settings.sound_enabled = values['-SOUND-']

    if event == '-SLIDER-':
        settings.sound_volume = values['-SLIDER-']
        
    if event == '-TOGGLE-':
        dark_mode = values['-TOGGLE-']

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break


# Close the window and exit the program
is_valid, error_msg = handler.config_valid()
if is_valid:
    handler.save_config()

write_settings_to_file(settings)
    
window.close()