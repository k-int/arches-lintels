import os
import json

from arches_lintels.settings import PG_USER, PG_ENCODING, PG_PORT
from arches_lintels.models.settings_model import SettingsModel


class NodeModel:
    def __init__(self):
        self.settings_model = SettingsModel()
        self.nodejs_path = self.settings_model.get_config_value(["dependencies","nodejs","install_directory"])

    def get_node_path(self):
        """
        NodeJS doesn't have a bin/ dir unlike psql or ES, so we just return the top level containing
        npm, npx, and node.exe.
        """
        return os.path.join(self.nodejs_path, "node.exe")

