import os
import json
import urllib.request

from arches_lintels.settings import ES_PORT
from arches_lintels.models.settings_model import SettingsModel


class ElasticsearchModel():
    def __init__(self):
        self.settings_model = SettingsModel()
        self.elasticsearch_path = self.settings_model.get_config_value(["dependencies","elasticsearch","install_directory"])

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
        args = ["/c", es_bat, "-E", f"http.port={ES_PORT}"]

        return primary_cmd, args, self.elasticsearch_path

    def verify_es_connection(self):
        """
        Pings elasticsearch to see if it's running.
        """
        # Replace 9200 with your custom port if you change it
        url = f"http://localhost:{ES_PORT}"
        
        # try:
            # Set a short timeout so the UI doesn't hang waiting
        with urllib.request.urlopen(url, timeout=2) as response:
            print(response.getcode())
            # if response.getcode() == 200:
            #     data = json.loads(response.read().decode())
            #     print(f"[ES Verification Success]: Cluster is up. Tagline: '{data.get('tagline')}'")
            #     return True
        # except Exception as e:
        #     # This will fail silently while ES is still booting up
        #     print("[ES Verification]: Waiting for cluster to respond...")
        #     return False