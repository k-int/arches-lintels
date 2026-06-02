import os

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import QDir, QSize
from PyQt6.QtWidgets import QDialog, QWidget

from arches_lintels.settings import ARCHES_VERSIONS, ARCHES_APPS, ONTOLOGIES
from arches_lintels.views.ui_active_project_widget import Ui_ActiveProjectWidget 


class ActiveProjectWidget(QWidget):
    """

    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_ActiveProjectWidget()
        self.ui.setupUi(self)
