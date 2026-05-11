import os
import json

class SettingsModel:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.app_root = os.path.join(self.root_dir, "arches_lintels")

        # self.config_path = os.path.join(self.app_root, "lintels_settings.json")
        # self.state = self.load_config()