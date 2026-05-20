from PyQt6.QtCore import QProcess

from functools import partial


from arches_lintels.models.settings_model import SettingsModel
from arches_lintels.models.dependencies.postgres import PostgresModel
from arches_lintels.controllers.components.file_browser import file_browser
from arches_lintels.controllers.utils.update_widget_styling import update_widget_styling


class ControlCentreController():
    """
    Controller for the stackedwidget control centre page
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.settings_model = SettingsModel()

        # dependencies
        self.postgres_model = PostgresModel()

        # app init configuration
        if self.postgres_model.pg_init_check():
            self.default_installed()
        else:
            self.default_not_installed()

        self.ui.postgresInstallButton.clicked.connect(self.initialise_postgres)
        self.ui.postgresRunButton.clicked.connect(self.start_postgres)
        self.ui.postgresStopButton.clicked.connect(self.stop_postgres)

    def default_installed(self):
        self.ui.postgresInstalledLabel.setText("Installed")
        update_widget_styling(self.ui.postgresInstalledLabel, "installed", "True")
        self.ui.postgresInstallButton.setEnabled(False)
        self.ui.postgresInstallButton.hide()
        self.ui.postgresRunButton.show()
        self.ui.postgresRunButton.setEnabled(True)
        self.ui.postgresStopButton.setEnabled(False)
        self.ui.postgresStopButton.hide()

    def default_not_installed(self):
        self.ui.postgresInstalledLabel.setText("Not installed")
        self.ui.postgresInstallButton.show()
        self.ui.postgresInstallButton.setText("Install")
        update_widget_styling(self.ui.postgresInstalledLabel, "installed", "False")
        # If not installed then also not running
        self.ui.postgresInstallButton.setEnabled(True)
        self.ui.postgresRunButton.show()
        self.ui.postgresRunButton.setEnabled(False)
        self.ui.postgresRunningLabel.setText("Not running")
        update_widget_styling(self.ui.postgresRunningLabel, "running", "False")
        self.ui.postgresStopButton.setEnabled(False)
        self.ui.postgresStopButton.hide()

    def default_running(self):
        """
        When running the start button should be hidden and the stop button visible.
        """
        update_widget_styling(self.ui.postgresRunningLabel, "running", "True")
        self.ui.postgresRunningLabel.setText("Running")
        self.ui.postgresRunButton.setEnabled(False)
        self.ui.postgresRunButton.hide()
        self.ui.postgresStopButton.setEnabled(True)
        self.ui.postgresStopButton.show()

    def default_starting(self):
        """
        When starting the stop button should be visible but disabled, the start button
        should be hidden and disabled.
        """
        update_widget_styling(self.ui.postgresRunningLabel, "starting", "True")
        self.ui.postgresRunningLabel.setText("Starting")
        self.ui.postgresRunButton.setEnabled(False)
        self.ui.postgresRunButton.hide()
        self.ui.postgresStopButton.setEnabled(False)
        self.ui.postgresStopButton.show()

    def default_not_running(self):
        """
        When not running the start button should be visible and stop hidden.
        """
        update_widget_styling(self.ui.postgresRunningLabel, "running", "False")
        self.ui.postgresRunningLabel.setText("Not running")
        self.ui.postgresRunButton.setEnabled(True)
        self.ui.postgresRunButton.show()
        self.ui.postgresStopButton.setEnabled(False)
        self.ui.postgresStopButton.hide()

    def initialise_postgres(self):
        """
        Initialise psql in a QProcess, call postgres model init function.
        """

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
            self.default_not_installed()
        self.default_installed()


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
        self.default_not_running()

        if self.pg_process and self.pg_process.state() == QProcess.ProcessState.Running:
            print("Stopping PostgreSQL...")
            self.pg_process.terminate()  # Sends a safe shutdown signal
            
            if not self.pg_process.waitForFinished(5000):
                self.pg_process.kill()

    def pg_state_change(self, state):
        """Responds to changes in the database process life cycle."""
        if state == QProcess.ProcessState.Starting:
            # self.default_starting()
            print("PostgreSQL is booting up... (Yellow Light)")

        elif state == QProcess.ProcessState.Running:
            self.default_running()
            print("PostgreSQL is running successfully! (Green Light)")

        elif state == QProcess.ProcessState.NotRunning:
            self.default_not_running()
            print("PostgreSQL has stopped. (Red Light)")

    def read_postgres_stderr(self):
        error_message = bytes(self.pg_process.readAllStandardError()).decode()
        print(f"[Postgres STDERR]: {error_message}")

    def read_postgres_stdout(self):
        output_message = bytes(self.pg_process.readAllStandardOutput()).decode()
        print(f"[Postgres STDOUT]: {output_message}")

    def handle_process_error(self, error):
        print(f"[QProcess Error Code]: {error}")        