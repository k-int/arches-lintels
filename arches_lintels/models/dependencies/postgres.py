import os
import json

from arches_lintels.settings import PG_USER, PG_ENCODING, PG_PORT
from arches_lintels.models.settings_model import SettingsModel


class PostgresModel:
    def __init__(self, settings_model):
        self.settings_model = settings_model
        self.postgres_path = self.settings_model.get_config_value(["dependencies","postgres","install_directory"])
        self.postgis_path = self.settings_model.get_config_value(["dependencies","postgis","install_directory"])

    def get_pg_bin_path(self):
        # todo need some os.path.exists() alerts here
        return os.path.join(self.postgres_path, "pgsql", "bin")

    def get_pg_data_path(self):
        return os.path.join(self.postgres_path, "pgsql", "data")

    def get_pg_createdb_path(self):
        return os.path.join(self.get_pg_bin_path(), "createdb.exe")

    def get_psql_path(self):
        return os.path.join(self.get_pg_bin_path(), "psql.exe")

    def pg_init_check(self):
        data_dir = self.get_pg_data_path()
        exists = os.path.exists(os.path.join(data_dir, "PG_VERSION"))
        # if data/PG_VERSION doesn't exist then tell settings psql is not installed
        self.settings_model.update_value(["dependencies","postgres","installed"], exists)
        # if it doesn't exist, set postgis installed to false
        if not exists:
            self.settings_model.update_value(["dependencies","postgis","installed"], False)
        return exists

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
            print(f"PostgreSQL initialisation failed with exit code: {exit_code}: {exit_status}")
            self.settings_model.update_value(["dependencies","postgres","installed"], False)

    def start_postgres(self):
        if not self.pg_init_check():
            print("Error: database not initialised")
            return

        postgres_exe = os.path.join(self.get_pg_bin_path(), "postgres.exe")
        data_dir = self.get_pg_data_path()

        args = ["-D", data_dir, "-p", PG_PORT]

        return postgres_exe, args

    def on_postgres_stopped(self, exit_code, exit_status):
        print("PostgreSQL has stopped (Red Light).")
        self.pg_process = None

    def closeEvent(self, event):
        """Overrides the window exit event to ensure we don't leave zombie databases."""
        self.stop_postgres()
        event.accept()

    def load_postgis_extension(self):
        """
        PSQL commands for loading the PostGIS extension.
        Note this uses the following commands from the Arches ubuntu install script:
            sudo -u postgres createdb -E UTF8 -T template0 --locale=en_US.utf8 template_postgis
            sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis'"
            sudo -u postgres psql -d template_postgis -c "CREATE EXTENSION postgis;"
            sudo -u postgres psql -d template_postgis -c "CREATE EXTENSION \"uuid-ossp\";"
            sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
            sudo -u postgres psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
            sudo -u postgres psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
        """
        
        createdb_exe = self.get_pg_createdb_path()
        psql_exe = self.get_psql_path()
        create_args = [
            "-U", "postgres",
            "-p", PG_PORT,
            "-E", "UTF8",
            "-T", "template0",
            "template_postgis"
        ]
        template_set_args = [
            "-U", "postgres",
            "-p", PG_PORT,
            "-d", "postgres",
            "-c", "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
        ]
        postgis_args = [
            "-U", "postgres",
            "-p", PG_PORT,
            "-T", "template_postgis",
            "-c", (
                "CREATE EXTENSION IF NOT EXISTS postgis; "
                "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"; "
                "GRANT ALL ON geometry_columns TO PUBLIC; "
                "GRANT ALL ON geography_columns TO PUBLIC; "
                "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
            )
        ]
        return createdb_exe, psql_exe, create_args, template_set_args, postgis_args
    
    def on_init_postgis_finished(self, exit_code, exit_status):
        if exit_code == 0:
            print("PostGIS initialised successfully")
            self.settings_model.update_value(["dependencies","postgis","installed"], True)
        else:
            print(f"PostGIS initialisation failed with exit code: {exit_code}: {exit_status}")
            self.settings_model.update_value(["dependencies","postgis","installed"], False)

    def postgis_bundled_check(self):
        """
        Checks if the PostGIS extension is bundled in the current PSQL installation.
        """
        exists = os.path.exists(os.path.join(self.postgres_path, "pgsql", "lib", "postgis-3.dll"))
        self.settings_model.update_value(["dependencies","postgis","bundled"], exists)
        return exists

    def postgis_install_check(self):
        """
        Checks if the PostGIS extension is installed in the current db.
        """
        return self.settings_model.get_config_value(["dependencies","postgis","installed"])
