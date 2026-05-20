import os
import json
import urllib.request

from arches_lintels.settings import ES_PORT
from arches_lintels.models.settings_model import SettingsModel


class ElasticsearchModel():
    def __init__(self):
        self.settings_model = SettingsModel()
        self.elasticsearch_path = self.settings_model.get_config_value(["dependencies","elasticsearch","install_directory"])
        self.max_retries = 15

    def get_es_bat_path(self):
        bat_path = os.path.join(self.elasticsearch_path, "bin", "elasticsearch.bat")
        if os.path.exists(bat_path):
            self.settings_model.update_value(["dependencies","elasticsearch","installed"], True)
        else:
            self.settings_model.update_value(["dependencies","elasticsearch","installed"], False)

        return os.path.join(self.elasticsearch_path, "bin", "elasticsearch.bat")

    def start_elasticsearch(self):
        print("STARTING ELASTICSEARCH")

        es_bat = self.get_es_bat_path()

        # Target cmd.exe instead of the batch file directly
        primary_cmd = "cmd.exe"
        args = [
            "/c",
            es_bat,
            f"-Ehttp.port={ES_PORT}",
            "-Expack.security.enabled=false",
            # "-Ediscovery.type=single-node",
        ]

        return primary_cmd, args, self.elasticsearch_path

    def elasticsearch_health(self, count):
        url = f"http://localhost:{ES_PORT}"
        count +=1

        try:
            with urllib.request.urlopen(url, timeout=1.5) as response:
                if response.getcode() == 200:
                    return True, count
        except Exception as e:
            print(f"Attempt {count}/{self.max_retries}...")
        
        if count >= self.max_retries:
            return False, count

        return None, count