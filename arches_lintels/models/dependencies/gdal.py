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
        # Here we replace the windows path with the ubuntu one to prevent settings_local.py error
        return os.path.join(self.get_gdal_path, "bin", "gdal.dll").replace("\\","/")
    
    @property
    def get_geos_c_dll(self):
        # Here we replace the windows path with the ubuntu one
        return os.path.join(self.get_gdal_path, "bin", "geos_c.dll").replace("\\","/")