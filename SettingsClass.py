
#            'BACKGROUND': '#222222',
#            'TEXT': '#ffff00',
#            'INPUT': '#fff0f0',
#            'TEXT_INPUT': '#0000ff',
#            'SCROLL': '#00ff00',
#            'BUTTON': ('#ff0000', '#00ffff'),
#            'PROGRESS': ('#0f0f0f', '#f0f0f0'),
#            'BORDER': 10,
#            'SLIDER_DEPTH': 0,
#            'PROGRESS_DEPTH': 0,
#            #'RELIEF': sg.RELIEF_FLAT,
#            #'FONT': textFont,
#            #'icon': 'res//images//SavegameManager.ico'

class Settings:
    settings_file = 'SavegameManagerSettings.json'

    def __init__(self):
        self.copy_config = True
        self.sound_enabled = True
        self.sound_volume: int = 100
        self.savegame_location = ''
        self.backup_location = ''
        self.theme = {
            'BACKGROUND': '#444444',
            'TEXT': '#ffffff',
            'INPUT': '#444444',
            'TEXT_INPUT': '#0000ff',
            'SCROLL': '#222222',
            'BUTTON': ('#ffffff', '#444444'),
            'PROGRESS': ('#0f0f0f', '#f0f0f0'),
            'BORDER': 1,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0,
            'RELIEF': 'flat'
            #'FONT': textFont,
            #'icon': 'res//images//SavegameManager.ico'
        }

    @property
    def sound_volume(self):
        return self._sound_volume

    @sound_volume.setter
    def sound_volume(self, value):
        self._sound_volume = max(0, min(value, 100))