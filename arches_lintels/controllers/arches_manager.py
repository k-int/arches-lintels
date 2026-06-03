import sys
import logging

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QProcess

from functools import partial

from arches_lintels.models.arches_model import ArchesModel
from arches_lintels.controllers.components.create_arches_project import CreateArchesProjectDialog
from arches_lintels.controllers.components.active_project_widget import ActiveProjectWidget
from arches_lintels.controllers.utils.qprocess_debugging import qprocess_debugging

logger = logging.getLogger(__name__)

class ArchesManagerController:
    """
    Controller for the stackedwidget Arches manager page
    """

    def __init__(self, ui, settings_model):
        super().__init__()
        self.ui = ui
        self.settings_model = settings_model
        self.arches_model = ArchesModel(settings_model)

        self.init_projects_ui()

        self.ui.createArchesProjectButton.disconnect()
        self.ui.createArchesProjectButton.clicked.connect(self.create_project)

    def init_projects_ui(self):
        projects = self.arches_model.get_projects()
        if len(projects) > 0:
            self.ui.noActiveProjectsLayout.hide()

            for project in projects:
                widget = ActiveProjectWidget()
                self.ui.projectLayout.addWidget(widget)
        else:
            self.ui.noActiveProjectsLayout.show()
            # self.ui.projectsLayout.hide()

    def create_project(self):
        print("CLICKED")
        self.create_project_dialog = CreateArchesProjectDialog()
        create_proj_result = self.create_project_dialog.exec()

        if create_proj_result == QDialog.DialogCode.Accepted:
            data = self.create_project_dialog.data

            project_dict = self.arches_model.new_project_entry(data["project_name"], data["arches_version"])
            python_exe, args = self.arches_model.create_virtual_environment(project_dict["venv_dir"])

            self.init_venv_process = QProcess()

            qprocess_debugging(self.init_venv_process)
            self.init_venv_process.finished.connect(
               partial(self.install_arches, project_dict=project_dict)
            )
            self.init_venv_process.start(python_exe, args)

    def install_arches(self, exit_code, exit_status, project_dict):
        if exit_code != 0:
            print("Failed to create vrtual environment", exit_code, exit_status)
            # todo remove from projects list? - don't want uncomplete projects clogging up list
            return

        venv_python_exe, args = self.arches_model.install_arches(venv_dir=project_dict["venv_dir"],
                                         arches_version=project_dict["arches_version"])

        self.arches_install_process = QProcess()
        qprocess_debugging(self.arches_install_process)
        self.arches_install_process.finished.connect(partial(self.create_arches_project, project_dict=project_dict))
        self.arches_install_process.start(venv_python_exe, args)

    # def on_install_arches_finished(self, exit_code, exit_status, project_dict):
    #     if exit_code !=0:
    #         print("Failed to install Arches", exit_code, exit_status)
    #         return

    #     project_dict

    def create_arches_project(self, exit_code, exit_status, project_dict):
        if exit_code !=0:
            print("Failed to install Arches", exit_code, exit_status)
            return

        print("project_dict", project_dict)
        arches_admin_exe, args = self.arches_model.create_new_project(
            venv_dir=project_dict["venv_dir"], 
            project_name=project_dict["name"],
            arches_project_dir=project_dict["arches_project_dir"]
        )

        self.create_project_process = QProcess()
        qprocess_debugging(self.create_project_process)
        self.create_project_process.start(arches_admin_exe, args)
