import os
import json

from arches_lintels.settings import PG_USER, PG_ENCODING, PG_PORT
from arches_lintels.models.settings_model import SettingsModel


class PostgresModel:
    def __init__(self):
        self.settings_model = SettingsModel()
        self.postgres_path = self.settings_model.get_config_value(["dependencies","postgres","install_directory"])

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
            self.settings_model.update_value(["dependencies","postgres","installed"], True)
        else:
            print(f"PostgreSQL initialisation failed with exit code: {exit_code}")

    def start_postgres(self):
        if not self.pg_init_check():
            print("Error: database not initialised")
            return

        postgres_exe = os.path.join(self.get_pg_bin_path(), "postgres.exe")
        data_dir = self.get_pg_data_path()

        args = ["-D", data_dir, "-p", PG_PORT]

        return postgres_exe, args

    # def stop_postgres(self):
    #     """Gracefully terminates the background database process."""
    #     if self.pg_process and self.pg_process.state() == QProcess.ProcessState.Running:
    #         print("Stopping PostgreSQL...")
    #         self.pg_process.terminate()  # Sends a safe shutdown signal
            
    #         # Wait up to 5 seconds for a clean shutdown, force kill if frozen
    #         if not self.pg_process.waitForFinished(5000):
    #             self.pg_process.kill()

    def on_postgres_stopped(self, exit_code, exit_status):
        print("PostgreSQL has stopped (Red Light).")
        self.pg_process = None

    def closeEvent(self, event):
        """Overrides the window exit event to ensure we don't leave zombie databases."""
        self.stop_postgres()
        event.accept()            