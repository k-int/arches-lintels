from functools import partial

from arches_lintels.models.settings_model import SettingsModel
from arches_lintels.controllers.components.file_browser import file_browser


class SettingsPage:
    """
    Controller for the stackedwidget settings page
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.settings = SettingsModel()

        self.ui.filePathLintels.setText(self.settings.get_config_value(["install_directory"]))
        self.ui.filePathPython.setText(self.settings.get_config_value(["dependencies","python","install_directory"]))
        self.ui.filePathPostgres.setText(self.settings.get_config_value(["dependencies","postgres","install_directory"]))
        self.ui.filePathElastic.setText(self.settings.get_config_value(["dependencies","elasticsearch","install_directory"]))
        self.ui.filePathNodejs.setText(self.settings.get_config_value(["dependencies","nodejs","install_directory"]))

        self.ui.fileBrowseLintels.clicked.connect(
            partial(self.select_folder,
                    self.ui.filePathLintels,
                    ["install_directory"])
        )
        self.ui.fileBrowsePython.clicked.connect(
            partial(self.select_folder,
                    self.ui.filePathPython,
                    ["dependencies","python","install_directory"])
        )
        self.ui.fileBrowsePostgres.clicked.connect(
            partial(self.select_folder,
                    self.ui.filePathPostgres,
                    ["dependencies","postgres","install_directory"])
        )
        self.ui.fileBrowseElastic.clicked.connect(
            partial(self.select_folder,
                    self.ui.filePathElastic,
                    ["dependencies","elasticsearch","install_directory"])
        )
        self.ui.fileBrowseNodejs.clicked.connect(
            partial(self.select_folder,
                    self.ui.filePathNodejs,
                    ["dependencies","nodejs","install_directory"])
        )


    def select_folder(self, line_edit, keys):
        folder_path = file_browser(dir_only=True)
        line_edit.setText(folder_path)
        self.settings.update_value(keys, folder_path)

