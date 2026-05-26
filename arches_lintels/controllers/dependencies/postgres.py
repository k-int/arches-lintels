from PyQt6.QtCore import QProcess

from arches_lintels.models.dependencies.postgres import PostgresModel
from arches_lintels.controllers.utils.process_debugging import read_stderr, read_stdout, handle_process_error
from arches_lintels.controllers.dependencies.dep_ui_updates import DependencyUIUpdates

class PostgresController():
    """
    Controller for the postgres processes.
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.dep_ui_updates = DependencyUIUpdates(
            install_label=self.ui.postgresInstalledLabel, 
            install_button = self.ui.postgresInstallButton, 
            start_button = self.ui.postgresRunButton, 
            stop_button = self.ui.postgresStopButton,
            running_label = self.ui.postgresRunningLabel
        )

        self.postgres_model = PostgresModel()

        # TODO: Change this to look at settings.json rather than the path existing
        if self.postgres_model.pg_init_check():
            self.dep_ui_updates.default_installed()
        else:
            self.dep_ui_updates.default_not_installed()

    def initialise_postgres(self):
        """
        Initialise psql in a QProcess, call postgres model init function.
        """
        print("init postgres")
        initdb_exe, args = self.postgres_model.initialise_postgres()

        self.init_process = QProcess()
        self.init_process.start(initdb_exe, args)
        self.init_process.finished.connect(
            self.on_init_postgres_finished
        )

    def on_init_postgres_finished(self, exit_code, exit_status):
        """
        Function for the controller to call the model on_init_postgres_finished 
        with additional UI modifications.
        """
        self.postgres_model.on_init_postgres_finished(exit_code, exit_status)
        if not exit_code == 0:
            self.dep_ui_updates.default_not_installed()
        self.dep_ui_updates.default_installed()

    def initialise_postgis_extension(self):
        def _additional_commands(exit_code, exit_status):
            print("additionals")
            if not exit_code == 0:
                print(f"failed with exit code: {exit_code}: {exit_status}")
                return
            self.init_postgis_process = QProcess()
            self.init_postgis_process.start(psql_exe, postgis_args)
            self.init_postgis_process.finished.connect(self.on_init_postgis_finished)

        def _template_set(exit_code, exit_status):
            if not exit_code == 0:
                print(f"failed with exit code: {exit_code}: {exit_status}")
                return            
            self.init_postgis_process = QProcess()
            self.init_postgis_process.start(psql_exe, template_set_args)
            self.init_postgis_process.finished.connect(_additional_commands)

        created_exe, psql_exe, create_args, template_set_args, postgis_args = self.postgres_model.load_postgis_extension()

        self.init_postgis_process = QProcess()
        self.init_postgis_process.start(created_exe, create_args)
        self.init_postgis_process.finished.connect(_template_set)

    def on_init_postgis_finished(self, exit_code, exit_status):
        self.postgres_model.on_init_postgis_finished(exit_code, exit_status)
        if not exit_code == 0:
            self.dep_ui_updates.default_not_installed()
        self.dep_ui_updates.default_installed()

    def start_postgres(self):
        postgres_exe, args = self.postgres_model.start_postgres()

        self.pg_process = QProcess()

        self.pg_process.stateChanged.connect(self.pg_state_change)
        self.pg_process.finished.connect(self.stop_postgres)

        # self.pg_process.readyReadStandardError.connect(self.read_postgres_stderr)
        # self.pg_process.readyReadStandardOutput.connect(self.read_postgres_stdout)
        # self.pg_process.errorOccurred.connect(self.handle_process_error)
        self.pg_process.start(postgres_exe, args)

    def stop_postgres(self):
        self.dep_ui_updates.default_not_running()

        if self.pg_process and self.pg_process.state() == QProcess.ProcessState.Running:
            print("Stopping PostgreSQL...")
            self.pg_process.terminate()  # Sends a safe shutdown signal
            
            if not self.pg_process.waitForFinished(5000):
                self.pg_process.kill()

    def pg_state_change(self, state):
        """Responds to changes in the database process life cycle."""
        if state == QProcess.ProcessState.Starting:
            self.dep_ui_updates.default_starting()
            print("PostgreSQL is booting up... (Yellow Light)")

        elif state == QProcess.ProcessState.Running:
            print("PostgreSQL is running successfully! (Green Light)")
            if not self.postgres_model.postgis_install_check():
                self.initialise_postgis_extension()
            self.dep_ui_updates.default_running()    

        elif state == QProcess.ProcessState.NotRunning:
            self.dep_ui_updates.default_not_running()
            print("PostgreSQL has stopped. (Red Light)")
