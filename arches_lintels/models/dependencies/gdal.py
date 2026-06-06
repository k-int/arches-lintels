import os
import logging

logger = logging.getLogger(__name__)

class GdalModel:
    def __init__(self, settings_model):
        self.settings_model = settings_model

    @property
    def get_gdal_path(self):
        return self.settings_model.get_config_value(["dependencies","gdal","install_directory"])

    @property
    def get_gdal_dll(self):
        return os.path.join(self.get_gdal_path, "bin", "gdal.dll")