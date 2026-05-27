from functools import partial

from arches_lintels.models.settings_model import SettingsModel
from arches_lintels.models.arches_model import ArchesModel


class ArchesManagerController:
    """
    Controller for the stackedwidget Arches manager page
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.arches_model = ArchesModel()

        self.init_projects_ui()
        
    def init_projects_ui(self):
        if len(self.arches_model.get_projects()) > 0:
            self.ui.noActiveProjectsLayout.hide()
            self.ui.projectsLayout.show()
        else:
            self.ui.noActiveProjectsLayout.show()
            self.ui.projectsLayout.hide()