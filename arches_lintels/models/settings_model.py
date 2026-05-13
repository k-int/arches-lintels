import os
import json

class SettingsModel:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.app_root = os.path.join(self.root_dir, "arches_lintels")

        self.settings_file_path = os.path.join(self.root_dir, "settings.json")    
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
        if not os.path.exists(self.settings_file_path):
            file_contents = self.defaults()
            self.save(file_contents)
        else:
            with open(self.settings_file_path, 'r') as f:
                file_contents = json.load(f)
        return file_contents

    def get_config_value(self, key):
        return self.settings_data.get(key)

    def update_value(self, key, value):
        self.settings_data[key] = value
        self.save(self.data)

    def save(self, data_to_save):
        with open(self.settings_file_path, 'w') as f:
            json.dump(data_to_save, f, )