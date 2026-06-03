import os
import json

from arches_lintels.settings import SYS_SETTINGS_PATH

class SettingsModel:
    def __init__(self, initialise_config=False):
        self.initialise_config = initialise_config
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
                "postgis": {
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
                },
                "gdal": {
                    "installed": False,
                    "install_directory": ""
                },
                "git": {
                    "installed": False,
                    "install_directory": ""
                },
            },
            "projects": [],
            "theme": "" #todo get from system default
        }

    def create_or_get_settings(self):
        if not os.path.exists(SYS_SETTINGS_PATH):
            file_contents = self.defaults()
            self.save(file_contents)
        else:
            with open(SYS_SETTINGS_PATH, 'r') as f:
                file_contents = json.load(f)

                # Check if existing settings is outdated & missing keys
                if self.initialise_config:
                    change, file_contents = self._update_existing_json_structure(file_contents)
                    if change: self.save(file_contents)

        return file_contents

    def _update_existing_json_structure(self, file_contents):
        # helper function for updating an existing settings.json 
        # file if the model structure changes.
        default = self.defaults()

        def find_diffs(default, file_contents, path=""):
            is_change = False
            for k in default:
                if k in file_contents:
                    if type(default[k]) is dict:
                        find_diffs(default[k],file_contents[k], "%s -> %s" % (path, k) if path else k)
                else:
                    file_contents[k] = default[k]
                    is_change = True
            return is_change

        result = find_diffs(default, file_contents)
        return result, file_contents

    def _get_conf_vals(self, keys):
        # helper function to get values despite any nesting
        settings_temp_copy = self.settings_data
        for key in keys:
            if isinstance(settings_temp_copy[key], dict):
                settings_temp_copy = settings_temp_copy[key]
            else:
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