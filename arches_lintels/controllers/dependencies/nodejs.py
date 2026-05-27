from PyQt6.QtCore import QProcess

from arches_lintels.models.dependencies.nodejs import NodeModel
from arches_lintels.controllers.utils.process_debugging import read_stderr, read_stdout, handle_process_error
from arches_lintels.controllers.dependencies.dep_ui_updates import DependencyUIUpdates

class nodeController():
    """
    Controller for the node processes.
    """

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.dep_ui_updates = DependencyUIUpdates(
            install_label=self.ui.nodeInstalledLabel, 
            install_button = self.ui.nodeInstallButton, 
            start_button = self.ui.nodeRunButton, 
            stop_button = self.ui.nodeStopButton,
            running_label = self.ui.nodeRunningLabel
        )

        self.node_model = NodeModel()
