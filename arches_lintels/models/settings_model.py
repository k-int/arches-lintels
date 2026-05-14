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

    def _get_conf_vals(self, keys):
        # helper function to get values despite any nesting
        settings_temp_copy = self.settings_data
        for key in keys:
            if isinstance(settings_temp_copy[key], dict):
                settings_temp_copy = settings_temp_copy[key]
                print("dict v", settings_temp_copy)
            else:
                print("in else, dict:", settings_temp_copy)
                print("key", settings_temp_copy[key])
                return settings_temp_copy[key]

    def _save_conf_vals(self, keys, value):
        # helper function to save values despite any nesting
        settings_temp_copy = self.settings_data
        for key in keys:
            if isinstance(settings_temp_copy[key], dict):
                settings_temp_copy = settings_temp_copy[key]
            else:
                settings_temp_copy[key] = value

    def get_config_value(self, keys):
        if not isinstance(keys, list):
            keys = keys.split()

        val = self._get_conf_vals(keys)
        return val

    def update_value(self, keys, value):
        if not isinstance(keys, list):
            keys = keys.split()

        self._save_conf_vals(keys, value)
        self.save(self.settings_data)

    def save(self, data_to_save):
        with open(SYS_SETTINGS_PATH, 'w') as f:
            json.dump(data_to_save, f, indent=4)