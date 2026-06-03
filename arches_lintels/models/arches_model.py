import os
import json
from uuid import uuid4
import datetime

from arches_lintels.settings import SYS_SETTINGS_PATH
from arches_lintels.models.settings_model import SettingsModel

class ArchesModel:
    def __init__(self, settings_model):
        self.settings_model = settings_model
        self.projects_root = os.path.join(self.get_lintels_path, "projects")

    @property
    def get_lintels_path(self):
        return self.settings_model.get_config_value("install_directory")

    @property
    def get_python_path(self):
        return self.settings_model.get_config_value(["dependencies", "python", "install_directory"])

    def get_projects(self):
        return self.settings_model.get_config_value("projects")
    
    def get_python_exe(self):
        return os.path.join(self.get_python_path, "python.exe")

    def _create_projects_root(self):
        os.makedirs(self.projects_root)

    def _is_venv_created(self, project_dir):
        """
        Look for the file venv/Scripts/activate, venv could have been created but not completed
        """
        return os.path.exists(os.path.join(project_dir, "venv", "Scripts", "activate"))

    def create_project_dir(self, project_name):
        if not os.path.exists(self.projects_root):
            self._create_projects_root()
        if not os.path.exists(os.path.join(self.projects_root, project_name)):
            os.makedirs(os.path.join(self.projects_root, project_name))
            return os.path.join(self.projects_root, project_name)
        else:
            print("Project name already exists: raise error here")
            return None

    def create_project_venv_dir(self, project_dir):
        os.makedirs(os.path.join(project_dir, "venv"))
        return os.path.join(project_dir, "venv")

    def new_project_entry(self, project_name, arches_version):
        project_dir = self.create_project_dir(project_name)
        venv_dir = self.create_project_venv_dir(project_dir)
        
        new_project = {
            "id": str(uuid4()),
            "name": project_name,
            "arches_version": arches_version,
            "arches_installed": False,
            "project_dir": project_dir,
            "project_created": False,
            "venv_dir": venv_dir,
            "venv_created": False,
            "created_at": str(datetime.datetime.now())
        }

        existing_projects = self.settings_model.get_config_value("projects")
        existing_projects.append(new_project)
        self.settings_model.update_value("projects", existing_projects)

        return new_project
    
    def create_virtual_environment(self, venv_dir):
        python_exe = self.get_python_exe()
        args = ["-m", "venv", venv_dir]
        return python_exe, args
    
    def install_arches(self, venv_dir, arches_version):
        venv_python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        args = ["-m", "pip", "install", f"arches~={arches_version}"]
        return venv_python_exe, args