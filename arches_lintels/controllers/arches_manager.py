import sys

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
        self.create_project_dialog.exec()
