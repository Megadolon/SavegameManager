import shutil
import os
from SettingsClass import Settings

class SavegameHandler:

    def __init__(self):
        self.src_path = None
        self.dest_path = None
        self.last_saves = []
    
    def set_config(self, _src_path, _dest_path):
        self.src_path = _src_path
        self.dest_path = _dest_path

    def load_config(self, settings):
        self.src_path = settings.savegame_location
        self.dest_path = settings.backup_location

    def has_sl2_file(self, folder_path):
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.lower().endswith('.sl2'):
                    return True
        return False

    def config_valid(self):
        if self.src_path is None:
            return False, "Source path is not set"

        if self.dest_path is None:
            return False, "Destination path is not set"

        if not os.path.exists(self.src_path):
            return False, "Source path does not exist"

        if not os.path.exists(self.dest_path):
            return False, "Destination path does not exist"

        if not self.has_sl2_file(self.src_path):
            return False, "No SL2 file found in source path"

        return True, None

    def find_highest_index(self):
        highest_index = -1
        for subfolder_name in os.listdir(self.dest_path):
            if subfolder_name.startswith("savegame_"):
                index_str = subfolder_name[len("savegame_"):]
                try:
                    index = int(index_str)
                    if index > highest_index:
                        highest_index = index
                except ValueError:
                    # If the numeric part of the folder name isn't a valid integer, skip it
                    pass
        return highest_index

    def save_data(self):
        if not os.path.exists(self.src_path) or not os.path.exists(self.dest_path):
            raise Exception("Both source and destination paths must exist.")
    
        src_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(self.src_path) for filename in filenames)
        if src_size > 100 * 1024 * 1024:
            raise Exception("Source directory is too large, it should be less than 100MB.")
    
        index = self.find_highest_index() + 1
        savegame_folder_name = f"savegame_{index}"
        save_folder = os.path.join(self.dest_path, savegame_folder_name)
        shutil.copytree(self.src_path, save_folder)
    
    def load_data(self):
        current = 0
        while True:
            index = self.find_highest_index() - current
            current += 1
            if index < 0:
                return
            savegame_folder_name = f"savegame_{index}"
            save_folder = os.path.join(self.dest_path, savegame_folder_name)
            if  os.path.exists(save_folder):
                if self.has_sl2_file(save_folder):
                    break
        if os.path.exists(self.src_path):
            shutil.rmtree(self.src_path)
            shutil.copytree(save_folder, self.src_path)