import os
import json

from arches_lintels.settings import SYS_SETTINGS_PATH
from arches_lintels.models.settings_model import SettingsModel

class ArchesModel:
    def __init__(self):
        self.settings = SettingsModel()

    def get_projects(self):
        return self.settings.get_config_value("projects")