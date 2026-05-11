import os
import json

class SettingsModel:
    def __init__(self):
        self.app_root = os.getcwd()
        self.project_root = os.path.join(self.app_root, "arches_lintels")

        print(self.app_root)

        # self.config_path = os.path.join(self.app_root, "lintels_settings.json")
        # self.state = self.load_config()