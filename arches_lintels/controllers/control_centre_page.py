from PyQt6.QtCore import QProcess

from functools import partial

from arches_lintels.utils.update_widget_styling import update_widget_styling

from arches_lintels.models.settings_model import SettingsModel
from arches_lintels.models.dependencies.postgres import PostgresModel
from arches_lintels.controllers.components.file_browser import file_browser


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

    def default_installed(self):
        self.ui.postgresInstalledLabel.setText("Installed")
        update_widget_styling(self.ui.postgresInstalledLabel, "installed", "True")
        self.ui.postgresInstallButton.setEnabled(False)
        self.ui.postgresInstallButton.hide()
        self.ui.postgresRunButton.setEnabled(True)

    def default_not_installed(self):
        self.ui.postgresInstalledLabel.setText("Not installed")
        self.ui.postgresInstallButton.show()
        self.ui.postgresInstallButton.setText("Install")
        update_widget_styling(self.ui.postgresInstalledLabel, "installed", "False")
        self.ui.postgresInstallButton.setEnabled(True)
        self.ui.postgresRunButton.setEnabled(False)
        self.ui.postgresRunningLabel.setText("Not running")
        update_widget_styling(self.ui.postgresRunningLabel, "running", "False")


    def initialise_postgres(self):
        initdb_exe, args = self.postgres_model.initialise_postgres()

        self.init_process = QProcess()
        self.init_process.start(initdb_exe, args)
        self.init_process.finished.connect(
            self.on_init_postgres_finished
        )

    def on_init_postgres_finished(self, exit_code, exit_status):
        """
        Function for the controller to call the model on_init_postgres_finished 
        with additional UI modifications"""
        self.postgres_model.on_init_postgres_finished(exit_code, exit_status)
        if not exit_code == 0:
            self.default_not_installed()
        self.default_installed()


    def start_postgres(self):
        postgres_exe, args = self.postgres_model.start_postgres()

        self.pg_process = QProcess()
        
        # Keep the background process invisible (prevents a black CMD box from popping up)
        # self.pg_process.setCreateProcessArgumentsModifier(
        #     lambda flags: flags | 0x08000000  # CREATE_NO_WINDOW flag
        # )
        self.pg_process.started.connect(lambda: print("PostgreSQL is running (Green Light)."))
        # self.pg_process.finished.connect(self.postgres_model.on_postgres_stopped)
        self.pg_process.start(postgres_exe, args)
