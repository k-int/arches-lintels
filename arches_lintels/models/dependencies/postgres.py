import os
import json

from arches_lintels.settings import PG_USER, PG_ENCODING
from arches_lintels.models.settings_model import SettingsModel


class PostgresModel:
    def __init__(self):
        self.postgres_path = SettingsModel().get_config_value(["dependencies","postgres","install_directory"])

    def get_pg_bin_path(self):
        # todo need some os.path.exists() alerts here
        return os.path.join(self.postgres_path, "pgsql", "bin")

    def get_pg_data_path(self):
        return os.path.join(self.postgres_path, "pgsql", "data")

    def pg_init_check(self):
        data_dir = self.get_pg_data_path()
        return os.path.exists(os.path.join(data_dir, "PG_VERSION"))

    def initialise_postgres(self):
        initdb_exe = os.path.join(self.get_pg_bin_path(), "initdb.exe")
        data_dir = self.get_pg_data_path()

        args = ["-D", data_dir, "-U", PG_USER, "-A", "trust", "-E", PG_ENCODING]

        return initdb_exe, args

    def on_init_postgres_finished(self, exit_code, exit_status):
        if exit_code == 0:
            print("PostgreSQL initialised successfully")
        else:
            print(f"PostgreSQL initialisation failed with exit code: {exit_code}")        