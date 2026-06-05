import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import QDir, QSize
from PyQt6.QtWidgets import QDialog, QWidget

from arches_lintels.settings import ARCHES_VERSIONS, ARCHES_APPS, ONTOLOGIES
from arches_lintels.views.ui_active_project_widget import Ui_ActiveProjectWidget 
from arches_lintels.controllers.components.progress_bar import progress_bar_ui


class ActiveProjectWidget(QWidget):
    """

    """

    def __init__(self, project_dict, project_key):
        super().__init__()
        self.ui = Ui_ActiveProjectWidget()
        self.ui.setupUi(self)

        self.ui.projectNameLabel.setText(project_key)
        self.ui.progressBar.hide()
        self.ui.messageLabel.hide()

    def start_step(self, text):
        self.set_message(text)
        self.set_progress_bar()

    def stop_step(self):
        self.ui.progressBar.hide()
        self.ui.messageLabel.hide()
        self.ui.messageLabel.setText("")

    def set_message(self, text):
        self.ui.messageLabel.show()
        self.ui.messageLabel.setText(text)

    def set_progress_bar(self):
        self.ui.progressBar.show()
        progress_bar_ui(self.ui.progressBar)