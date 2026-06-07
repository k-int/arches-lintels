import sys
import logging

from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QProcess

from functools import partial

from arches_lintels.models.arches_model import ArchesModel
from arches_lintels.models.dependencies.nodejs import NodeModel

from arches_lintels.controllers.dependencies.nodejs import node_environment
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
        self.node_model = NodeModel(settings_model)
        self.arches_model = ArchesModel(settings_model, self.node_model)

        self.init_projects_ui()

        self.ui.createArchesProjectButton.disconnect()
        self.ui.createArchesProjectButton.clicked.connect(self.create_project)

    def init_projects_ui(self):
        projects = self.arches_model.get_projects()
        if len(projects) > 0:
            self.ui.noActiveProjectsLayout.hide()

            for project_name, project_dict in projects.items():
                widget = self.new_proj_widget_create(project_dict=project_dict, project_key=project_name)
                self.new_proj_widget_add_to_layout(widget)
        else:
            self.ui.noActiveProjectsLayout.show()
            # self.ui.projectsLayout.hide()

    def new_proj_widget_create(self, project_dict, project_key):
        widget = ActiveProjectWidget(project_dict, project_key, self.settings_model)
        widget.run_project_signal.connect(partial(self.run_project, 
                                                project_dict=project_dict, 
                                                project_key=project_key, 
                                                widget=widget))
        return widget

    def new_proj_widget_add_to_layout(self, widget):
        self.ui.projectLayout.addWidget(widget)

    def create_project(self):
        self.create_project_dialog = CreateArchesProjectDialog(self.arches_model)
        create_proj_result = self.create_project_dialog.exec()

        if create_proj_result == QDialog.DialogCode.Accepted:
            data = self.create_project_dialog.data

            project_dict = self.arches_model.new_project_entry(data["project_name"], data["arches_version"], data)
            python_exe, args = self.arches_model.create_virtual_environment(project_dict["venv_dir"])

            # Create the new project widget and add to the layout 
            widget = self.new_proj_widget_create(project_dict=project_dict, project_key=data["project_name"])
            self.new_proj_widget_add_to_layout(widget)
            # Set message
            widget.start_step("Step 1/4: Creating virtual environment")

            self.init_venv_process = QProcess()

            qprocess_debugging(self.init_venv_process)
            self.init_venv_process.finished.connect(
               partial(self.install_arches, project_dict=project_dict, project_key=data["project_name"], widget=widget)
            )
            self.init_venv_process.start(python_exe, args)

    def install_arches(self, exit_code, exit_status, project_dict, project_key, widget):
        if exit_code != 0:
            print("Failed to create vrtual environment", exit_code, exit_status)
            self.settings_model.update_value(["projects", project_key, "venv_created"], False)
            # todo remove from projects list? - don't want uncomplete projects clogging up list
            return

        # set venv_created setting as True
        self.settings_model.update_value(["projects", project_key, "venv_created"], True)
        widget.stop_step()

        venv_python_exe, args = self.arches_model.install_arches(venv_dir=project_dict["venv_dir"],
                                         arches_version=project_dict["arches_version"])

        widget.start_step(f"Step 2/4: Installing Arches {project_dict['arches_version']} (this may take some time)")

        self.arches_install_process = QProcess()
        qprocess_debugging(self.arches_install_process)
        self.arches_install_process.finished.connect(partial(self.create_arches_project, 
                                                             project_dict=project_dict, 
                                                             project_key=project_key, 
                                                             widget=widget))
        self.arches_install_process.start(venv_python_exe, args)

    # def on_install_arches_finished(self, exit_code, exit_status, project_dict):
    #     if exit_code !=0:
    #         print("Failed to install Arches", exit_code, exit_status)
    #         return

    #     project_dict

    def create_arches_project(self, exit_code, exit_status, project_dict, project_key, widget):
        if exit_code !=0:
            print("Failed to install Arches", exit_code, exit_status)
            self.settings_model.update_value(["projects", project_key, "arches_installed"], False)
            return

        # set arches_installed setting as True
        self.settings_model.update_value(["projects", project_key, "arches_installed"], True)
        widget.stop_step()

        arches_admin_exe, args = self.arches_model.create_new_project(
            venv_dir=project_dict["venv_dir"], 
            project_name=project_key,
            arches_project_dir=project_dict["arches_project_dir"]
        )

        widget.start_step(f"Step 3/4: Creating Project (this may take some time)")

        self.create_project_process = QProcess()
        qprocess_debugging(self.create_project_process)

        qprocessenv = node_environment(self.node_model)
        self.create_project_process.setProcessEnvironment(qprocessenv)
        self.create_project_process.start(arches_admin_exe, args)
        self.create_project_process.finished.connect(partial(self.initialise_project, 
                                                             project_dict=project_dict,
                                                             project_key=project_key,
                                                             widget=widget))

    def initialise_project(self, exit_code, exit_status, project_dict, project_key, widget):
        if exit_code !=0:
            print("Failed to create project", exit_code, exit_status)
            self.settings_model.update_value(["projects", project_key, "project_created"], False)
            return

        # set project_created setting as True
        self.settings_model.update_value(["projects", project_key, "project_created"], True)
        widget.stop_step()

        venv_python_exe, args = self.arches_model.initialise_project(project_name=project_key, project_dict=project_dict)
        
        widget.start_step(f"Step 4/4: Initialising Project (this may take some time)")

        self.init_project_process = QProcess()
        qprocess_debugging(self.init_project_process)

        self.init_project_process.start(venv_python_exe, args)
        self.init_project_process.finished.connect(partial(self.on_initialise_project_finished, 
                                                             project_dict=project_dict,
                                                             project_key=project_key,
                                                             widget=widget))


    def on_initialise_project_finished(self, exit_code, exit_status, project_dict, project_key, widget):
        if exit_code !=0:
            print("Failed to init project", exit_code, exit_status)
            self.settings_model.update_value(["projects", project_key, "project_initialised"], False)
            return

        # set project_initialised setting as True
        self.settings_model.update_value(["projects", project_key, "project_initialised"], True)
        widget.stop_step()

    def run_project(self, project_dict, project_key, widget):
        venv_python_exe, args = self.arches_model.run_project(project_name=project_key, project_dict=project_dict)
        
        self.run_project_process = QProcess()
        qprocess_debugging(self.run_project_process)
        self.run_project_process.start(venv_python_exe, args)

        primary_cmd, npm_args = self.arches_model.run_npm_build_development()

        self.npm_build_dev_process = QProcess()
        self.npm_build_dev_process.setWorkingDirectory(project_dict["arches_project_dir"])

        callback_funct = partial(self._scan_for_webpack_completion, widget=widget)
        qprocess_debugging(self.npm_build_dev_process, stdout_callback=callback_funct)

        qprocessenv = node_environment(self.node_model)
        self.npm_build_dev_process.setProcessEnvironment(qprocessenv)
        self.npm_build_dev_process.start(primary_cmd, npm_args)
        widget.start_step("Starting Arches project server...")

    def _scan_for_webpack_completion(self, output_text, widget):
        if not self.npm_build_dev_process:
            return
        
        output_text = output_text.lower()
        
        if "compiled successfully" in output_text:
            widget.stop_step()
