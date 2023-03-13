import PySimpleGUI as sg
import keyboard
from SavegameHandlerClass import SavegameHandler
import pygame
import json
from SettingsClass import Settings
class Manager:
    def __init__(self, settings):
        self.settings = settings
        self.handler = SavegameHandler()
        self.handler.load_config(settings)

        self.is_open = True
        self.is_running=False

        self.set_theme(settings.theme)
        icon_path = 'res//images//SavegameManager.ico'

        sg.set_global_icon(icon_path)

        savegame_path = 'no path'
        backup_path = 'no path'
        valid, error = self.handler.config_valid()
        if valid:
            savegame_path = self.handler.src_path
            backup_path = self.handler.dest_path
        else:
            popup_window(error)

        _relief = 'flat'

        tab1_manager_layout = [
            [sg.Frame('Savegame Location', [
                [sg.Button('Select folder', key='-BUTTON-SELECT_SAVEGAME_FOLDER', size=(10,1)),
                 sg.Text(savegame_path, size=(80,1), relief=_relief,  key='-OUTPUT-SAVEGAME_FOLDER')]
            ], relief=_relief)],
            [sg.Frame('Backup Location', [
                [sg.Button('Select folder', key='-BUTTON-SELECT_BACKUP_FOLDER', size=(10,1)),
                 sg.Text(backup_path, size=(80,1), relief=_relief, key='-OUTPUT-BACKUP_FOLDER')]
            ], relief=_relief)],
            [sg.Frame('', [
                [sg.Button('Start', key='-BUTTON-START', size=(10,1)),
                 sg.Button('Stop', key='-BUTTON-STOP', size=(10,1), disabled=True)
                ]
            ], relief=_relief)]
        ]



        tab2_settings_layout =[
                        [sg.Checkbox('Sound', key='-TOGGLE-SOUND_ENABLED', size=(10,1), default=settings.sound_enabled, enable_events=True, metadata=True)],
                        [sg.Slider(range=(0, 1), orientation='horizontal', size=(20, 15), default_value=settings.sound_volume, resolution=0.01, enable_events=True, key='-SLIDER-')],
                        [sg.Checkbox('Copy Config', key='-TOGGLE-COPY_CONFIG', size=(10,1), default=True, enable_events=True, metadata=True)]
                    ]

        tabgroup_layout = [
            [sg.TabGroup([
                [sg.Tab('Manager', tab1_manager_layout, background_color='#888888', title_color='#ff0000')],
                [sg.Tab('Settings', tab2_settings_layout, background_color='#888888', title_color='#ff0000')]
            ], selected_background_color='#888888', selected_title_color='#ffffff')]
        ]

        self.window = sg.Window('Savegame Manager', tabgroup_layout, finalize=True)
        self.window.set_min_size((875, 175))
        self.run(False)
        #self.window.TKroot.configure()
        

    
    def __del__(self):
        self.window.close()
    
    def set_theme(self, theme):
        textFont = ('Arial', 5)

        sg.theme
        
        sg.theme_add_new('my_theme', theme)
        sg.theme('my_theme')

    def select_folder_callback(self, input_field, folder_type):
        folder_path = sg.popup_get_folder('Select a ' + folder_type + ' folder', default_path=self.window[input_field].get(), size=(80, 1))

        if folder_path:
            self.window[input_field].update(f'{folder_path}')

    def run(self, value: bool):
        enabled=('white', '#666666')
        disabled=('white', '#AAAAAA')

        self.window['-BUTTON-SELECT_SAVEGAME_FOLDER'].update(disabled=value)
        self.window['-BUTTON-SELECT_SAVEGAME_FOLDER'].update(button_color=enabled if value else disabled)
        self.window['-BUTTON-SELECT_BACKUP_FOLDER'].update(disabled=value)
        self.window['-BUTTON-SELECT_BACKUP_FOLDER'].update(button_color=enabled if value else disabled)
        self.window['-BUTTON-STOP'].update(disabled=not value)
        self.window['-BUTTON-STOP'].update(button_color=enabled if not value else disabled)
        self.window['-BUTTON-START'].update(disabled=value)
        self.window['-BUTTON-START'].update(button_color=enabled if value else disabled)

        self.is_running = value

    def update(self):
        event, values = self.window.read()

        # If the user closes the window or clicks the Exit button, exit the event loop
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            self.is_open = False

        # If the user clicks the button, call the button_callback function
        if event == '-BUTTON-SELECT_SAVEGAME_FOLDER':
            self.select_folder_callback('-OUTPUT-SAVEGAME_FOLDER', 'Savegame')

        if event == '-BUTTON-SELECT_BACKUP_FOLDER':
            self.select_folder_callback('-OUTPUT-BACKUP_FOLDER', 'Backup')

        if event == '-BUTTON-START':
            self.handler.set_config(self.window['-OUTPUT-SAVEGAME_FOLDER'].get(), self.window['-OUTPUT-BACKUP_FOLDER'].get())
            is_valid, error_msg = self.handler.config_valid()
            if is_valid:
                self.run(True)
            else:
                popup_window(error_msg)

        if event == '-BUTTON-STOP':
            self.run(False)

        if event == '-TOGGLE-SOUND_ENABLED':
            self.settings.sound_enabled = values['-TOGGLE-SOUND_ENABLED']

        if event == '-SLIDER-':
            self.settings.sound_volume = values['-SLIDER-']

        if event == '-TOGGLE-COPY_CONFIG':
            self.settings.copy_config = values['-TOGGLE-COPY_CONFIG']

    def on_press_f9(self, event):
        if not self.is_running:
            return
        if event.name == 'f9':
            self.handler.load_data()
            if self.settings.sound_enabled:
                play_audio(audio_load, self.settings.sound_volume)

    def on_press_f5(self, event):
        if not self.is_running:
            return
        if event.name == 'f5':
            self.handler.save_data()
            if self.settings.sound_enabled:
                play_audio(audio_save, self.settings.sound_volume)

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
    
def play_audio(audio, volume):
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()



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

audio_save = 'res//audio//save.wav'
audio_load = 'res//audio//load.wav'

def main():
    #settings = Settings()
    settings = read_settings_from_file()
    print(settings.savegame_location)
    print(settings.backup_location)
    manager = Manager(settings)
    

    pygame.init()

    keyboard.on_release(manager.on_press_f5)
    keyboard.on_release(manager.on_press_f9)
    # Start the event loop to process events and wait for user interaction
    while manager.is_open:

        manager.update()

    if manager.handler.config_valid():
        settings.savegame_location = manager.handler.src_path
        settings.backup_location = manager.handler.dest_path

    print(settings.savegame_location)
    print(settings.backup_location)

    write_settings_to_file(settings)

if __name__ == "__main__":
    main()

