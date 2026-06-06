import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import QDir, QSize
from PyQt6.QtWidgets import QDialog

from arches_lintels.settings import ARCHES_VERSIONS, ARCHES_APPS, ONTOLOGIES
from arches_lintels.views.ui_create_arches_project import Ui_CreateArchesProject


class CreateArchesProjectDialog(QDialog):
    """
    Arches create new project dialog interface
    """

    def __init__(self, arches_model):
        super().__init__()
        self.ui = Ui_CreateArchesProject()
        self.ui.setupUi(self)
        self.arches_model = arches_model

        self.init_ui()
        self.ui.createProjectButton.clicked.connect(self.create_project)
        self.ui.advancedButton.clicked.connect(self.open_advanced)
        self.ui.advancedOptions.setVisible(False)

    def init_ui(self):
        self.ui.archesVersions.clear()
        self.ui.archesVersions.addItems(ARCHES_VERSIONS)
        self.ui.archesApps.clear()
        # self.ui.archesApps.addItems(ARCHES_APPS) # not yet implemented 
        self.ui.ontologyCombo.clear()
        self.ui.ontologyCombo.addItem("None")
        self.ui.ontologyCombo.addItems(ONTOLOGIES)
        self.ui.ontologyCombo.setCurrentIndex(1) # set default to CIDOC

    def open_advanced(self):
        if self.ui.advancedButton.isChecked():
            self.ui.advancedOptions.setVisible(True)
        else:
            self.ui.advancedOptions.setVisible(False)

    def create_project(self):
        self.data = {
            "project_name": self.ui.archesProjectName.text(),
            "arches_version": self.ui.archesVersions.currentText(),
            "arches_apps": self.ui.archesApps.currentText(),
            "mapbox_api_key": self.ui.mapboxApiKey.text(),
            "ontology": self.ui.ontologyCombo.currentText(),
            "debug": self.ui.debugCheckBox.isChecked(),
            "accessibility_mode": self.ui.accessibilityCheckBox.isChecked()
        }

        validation_pass, error_msg = self.arches_model.new_project_validation(self.data)

        if not validation_pass:
            self.ui.errorMessageLabel.setText(error_msg)
            return

        # close dialog with 'Accepted' status
        self.accept()