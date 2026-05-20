from functools import partial

from arches_lintels.utils.update_widget_styling import update_widget_styling

from arches_lintels.models.settings_model import SettingsModel
from arches_lintels.models.dependencies.postgres import PostgresModel
from arches_lintels.controllers.components.file_browser import file_browser


class ControlCentreController:
    """
    Controller for the stackedwidget control centre page
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.postgres_model = PostgresModel()

        if self.postgres_model.pg_init_check():
            self.ui.postgresInstalledLabel.setText("Installed")
            update_widget_styling(self.ui.postgresInstalledLabel, "installed", "True")
        else:
            self.ui.postgresInstalledLabel.setText("Not installed")
            update_widget_styling(self.ui.postgresInstalledLabel, "installed", "False")