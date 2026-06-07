import os
import logging
from uuid import uuid4
import datetime

from arches_lintels.settings import ONTOLOGIES
from arches_lintels.models.dependencies.gdal import GdalModel
from arches_lintels.models.arches_components.settings_local_template import settings_local_template

logger = logging.getLogger(__name__)

class ArchesModel:
    def __init__(self, settings_model, node_model):
        self.settings_model = settings_model
        self.node_model = node_model
        self.gdal_model = GdalModel(self.settings_model)
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

    def create_lintel_project_dir(self, project_name):
        if not os.path.exists(self.projects_root):
            self._create_projects_root()
        if not os.path.exists(os.path.join(self.projects_root, project_name)):
            os.makedirs(os.path.join(self.projects_root, project_name))
            return os.path.join(self.projects_root, project_name)
        else:
            print("Project name already exists: raise error here")
            return None

    def create_arches_project_dir(self, lintel_project_dir, project_name):
        os.makedirs(os.path.join(lintel_project_dir, project_name))
        return os.path.join(lintel_project_dir, project_name)

    def create_project_venv_dir(self, project_dir):
        os.makedirs(os.path.join(project_dir, "venv"))
        return os.path.join(project_dir, "venv")

    def new_project_validation(self, data):
        if data["project_name"]:
            if ' ' in data["project_name"]:
                return False, "Error: project name should not contain any spaces"

            if data["project_name"] in self.settings_model.get_config_value("projects"):
                return False, "Error: Project with name already exists"
        
            return True, ""
        
        return False, "Error: Required fields not populated"

    def new_project_entry(self, project_name, arches_version, data):
        """
        Creates a new Arches project entry.
        Since validation occurs in a step prior to this, we can assume the project is valid and 
        ready to be added to settings.
        """
        lintel_project_dir = self.create_lintel_project_dir(project_name)
        venv_dir = self.create_project_venv_dir(lintel_project_dir)
        arches_project_dir = self.create_arches_project_dir(lintel_project_dir, project_name)

        new_project = {
            "arches_version": arches_version,
            "arches_installed": False,
            "lintel_project_dir": lintel_project_dir,
            "arches_project_dir": arches_project_dir,
            "project_created": False,
            "project_initialised": False,
            "venv_dir": venv_dir,
            "venv_created": False,
            "created_at": str(datetime.datetime.now()),
            "config": data
        }

        existing_projects = self.settings_model.get_config_value("projects")
        existing_projects[project_name] = new_project
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

    def create_new_project(self, venv_dir, project_name, arches_project_dir):
        # the use of archesadmin means we only support 7.6 onwards
        arches_admin_exe = os.path.join(venv_dir, "Scripts", "arches-admin.exe")
        args = ["startproject", project_name, "--directory", arches_project_dir]
        return arches_admin_exe, args

    def settings_local(self, project_name, project_dict):
        """
        Generates a settings_local.py file for Lintels dependencies
        """
        settings_local_path = os.path.join(project_dict["arches_project_dir"], project_name, "settings_local.py")
        
        with open(settings_local_path, "w") as f:
            f.write(settings_local_template(project_name, 
                                            project_dict["config"], 
                                            self.gdal_model.get_gdal_dll,
                                            self.gdal_model.get_geos_c_dll))
            logger.debug(f"settings_local.py file created at {settings_local_path}")

    def initialise_project(self, project_name, project_dict):
        self.settings_local(project_name, project_dict)

        venv_python_exe = os.path.join(project_dict["venv_dir"], "Scripts", "python.exe")
        manage_py = os.path.join(project_dict["arches_project_dir"], "manage.py")
        args = [manage_py, "setup_db", "--force"]
        return venv_python_exe, args
    
    def load_ontology(self, project_dict):
        venv_python_exe = os.path.join(project_dict["venv_dir"], "Scripts", "python.exe")
        manage_py = os.path.join(project_dict["project_dir"], "manage.py")

        proj_ontology = project_dict["config"]
        if proj_ontology:
            ontology_path = ONTOLOGIES[proj_ontology]

        args = [manage_py, "load_ontology", "-s", ontology_path]
        return venv_python_exe, args
    
    def run_project(self, project_name, project_dict):
        venv_python_exe = os.path.join(project_dict["venv_dir"], "Scripts", "python.exe")
        manage_py = os.path.join(project_dict["arches_project_dir"], "manage.py")
        args = [manage_py, "runserver", "8000"]
        return venv_python_exe, args
    
    def run_npm_build_development(self):
        npm_cmd = self.node_model.get_npm_cmd_path
        primary_cmd = "cmd.exe"

        args = [
            "/c",
            npm_cmd,
            "run",
            "start"
        ]

        return primary_cmd, args
    
    def stop_project(self, pid):
        command = "taskkill"
        args = ["/F", "/T", "/PID", str(pid)]

        return command, args
