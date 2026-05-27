import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import QDir, QSize
from PyQt6.QtWidgets import QDialog

from arches_lintels.settings import ARCHES_VERSIONS, ARCHES_APPS
from arches_lintels.views.ui_create_arches_project import Ui_CreateArchesProject


class CreateArchesProjectDialog(QDialog):
    """
    Arches create new project dialog interface
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_CreateArchesProject()
        self.ui.setupUi(self)
        self.init_ui()
        print("INIT")

    def init_ui(self):
        self.ui.archesVersions.clear()
        self.ui.archesVersions.addItems(ARCHES_VERSIONS)
        self.ui.archesApps.clear()
        self.ui.archesApps.addItems(ARCHES_APPS)

    