import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QWidget

from arches_lintels.settings import ARCHES_VERSIONS, ARCHES_APPS, ONTOLOGIES
from arches_lintels.views.ui_active_project_widget import Ui_ActiveProjectWidget 
from arches_lintels.controllers.components.progress_bar import progress_bar_ui


class ActiveProjectWidget(QWidget):
    """

    """

    run_project_signal = pyqtSignal(str)

    def __init__(self, project_dict, project_key, settings_model):
        super().__init__()
        self.ui = Ui_ActiveProjectWidget()
        self.ui.setupUi(self)
        self.settings_model = settings_model
        self.project_dict = project_dict
        self.project_key = project_key

        self.ui.projectRunButton.clicked.connect(self.run_button)

        self.ui.projectNameLabel.setText(project_key)
        self.setup_ui_buttons()

    def _hide_all(self):
        """
        Helper function to hide all widgets/labels.
        """
        self.ui.progressBar.hide()
        self.ui.messageLabel.hide()
        self.ui.projectConfigureButton.hide()
        self.ui.projectRunButton.hide()
        self.ui.projectVenvButton.hide()
        self.ui.projectCreateProjectButton.hide()
        self.ui.projectInstallArchesButton.hide()
        self.ui.projectInitButton.hide()

    def setup_ui_buttons(self):
        """
        This function sets up the buttons in the widget by looking at what stage 
        of installation the project is at.
        """
        self._hide_all()

        if not self.project_dict["venv_created"]:
            self.ui.messageLabel.setText("Virtual environment does not exist")
            self.ui.messageLabel.show()
            self.ui.projectVenvButton.show()
        elif not self.project_dict["arches_installed"]:
            self.ui.messageLabel.setText("Arches is not installed")
            self.ui.messageLabel.show()
            self.ui.projectInstallArchesButton.show()
        elif not self.project_dict["project_created"]:
            self.ui.messageLabel.setText("Project does not exist")
            self.ui.messageLabel.show()
            self.ui.projectCreateProjectButton.show()
        elif not self.project_dict["project_initialised"]:
            self.ui.messageLabel.setText("Project is not initialised")
            self.ui.messageLabel.show()
            self.ui.projectInitButton.show()
        else:
            # All values true, so can assume project exists and set up
            self.ui.projectRunButton.show()
            self.ui.projectConfigureButton.show()


    def start_step(self, text):
        self._hide_all()
        self.set_message(text)
        self.set_progress_bar()

    def stop_step(self):
        self.ui.progressBar.hide()
        self.ui.messageLabel.hide()
        self.ui.messageLabel.setText("")
        self.setup_ui_buttons()

    def set_message(self, text):
        self.ui.messageLabel.show()
        self.ui.messageLabel.setText(text)

    def set_progress_bar(self):
        self.ui.progressBar.show()
        progress_bar_ui(self.ui.progressBar)

    def run_button(self):
        self.run_project_signal.emit(self.project_key)