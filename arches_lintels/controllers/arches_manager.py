import sys

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QProcess

from functools import partial

from arches_lintels.models.arches_model import ArchesModel
from arches_lintels.controllers.components.create_arches_project import CreateArchesProjectDialog


class ArchesManagerController:
    """
    Controller for the stackedwidget Arches manager page
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.arches_model = ArchesModel()

        self.init_projects_ui()

        self.ui.createArchesProjectButton.disconnect()
        self.ui.createArchesProjectButton.clicked.connect(self.create_project)
        
    def init_projects_ui(self):
        if len(self.arches_model.get_projects()) > 0:
            self.ui.noActiveProjectsLayout.hide()
            self.ui.projectsLayout.show()
        else:
            self.ui.noActiveProjectsLayout.show()
            self.ui.projectsLayout.hide()

    def create_project(self):
        print("CLICKED")
        self.create_project_dialog = CreateArchesProjectDialog()
        create_proj_result = self.create_project_dialog.exec()

        if create_proj_result == QDialog.DialogCode.Accepted:
            data = self.create_project_dialog.data

            print(data)

            project_dict = self.arches_model.new_project_entry(data["project_name"], data["arches_version"])
            python_exe, args = self.arches_model.create_virtual_environment(project_dict["venv_dir"])

            self.init_venv_process = QProcess()
            self.init_venv_process.finished.connect(self.install_arches)
            self.init_venv_process.start(python_exe, args)

    
    def install_arches(self, exit_code, exit_status):
        if exit_code != 0:
            print("Failed to create vrtual environment")
            return
        