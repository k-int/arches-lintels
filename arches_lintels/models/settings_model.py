import os
import json

from arches_lintels.settings import SYS_SETTINGS_PATH

class SettingsModel:
    def __init__(self):
        self.settings_data = self.create_or_get_settings()

    def defaults(self):
        return {
            "install_directory": "",
            "dependencies": {
                "python": {
                    "installed": False,
                    "install_directory": ""
                },
                "postgres": {
                    "installed": False,
                    "install_directory": ""
                },
                "elasticsearch": {
                    "installed": False,
                    "install_directory": ""
                },
                "nodejs": {
                    "installed": False,
                    "install_directory": ""
                }
            },
            "projects": []
        }

    def create_or_get_settings(self):
        if not os.path.exists(SYS_SETTINGS_PATH):
            file_contents = self.defaults()
            self.save(file_contents)
        else:
            with open(SYS_SETTINGS_PATH, 'r') as f:
                file_contents = json.load(f)
        return file_contents

    def get_config_value(self, key):
        return self.settings_data.get(key)

    def update_value(self, key, value):
        self.settings_data[key] = value
        self.save(self.data)

    def save(self, data_to_save):
        with open(SYS_SETTINGS_PATH, 'w') as f:
            json.dump(data_to_save, f, )