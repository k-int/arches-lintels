import os

from PyQt6.QtGui import QIcon, QCursor, QPixmap, QTransform
from PyQt6.QtCore import QDir, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication

from arches_lintels.views.ui_mainwindow import Ui_MainWindow
from arches_lintels.models.settings_model import SettingsModel

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Lintels Main Window interface class
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.is_fullscreen = True

        settings = SettingsModel()

        QDir.addSearchPath("img", os.path.join(settings.project_root, "img"))

        self.homeButtonIconOnly.setIcon(QIcon("img:icons/fa-archway-solid-white.svg"))
        self.homeButtonIconOnly.setIconSize(QSize(20,20))
        self.homeFull.setIcon(QIcon("img:icons/fa-archway-solid-white.svg"))
        
        self.controlCentreIconOnly.setIcon(QIcon("img:icons/fa-bars-progress-solid-white.svg"))
        self.controlCentreIconOnly.setIconSize(QSize(20,20))
        self.controlCentreFull.setIcon(QIcon("img:icons/fa-bars-progress-solid-white.svg"))

        self.archesCentreIconOnly.setIcon(QIcon("img:Arches_icon_white.svg"))
        self.archesCentreIconOnly.setIconSize(QSize(20,20))
        self.archesCentreFull.setIcon(QIcon("img:Arches_icon_white.svg"))

        self.settingsIconOnly.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))
        self.settingsIconOnly.setIconSize(QSize(20,20))
        self.settingsFull.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))

        self.aboutIconOnly.setIcon(QIcon("img:icons/fa-circle-question-regular-white.svg"))
        self.aboutIconOnly.setIconSize(QSize(20,20))
        self.aboutFull.setIcon(QIcon("img:icons/fa-circle-question-regular-white.svg"))

        self.menuButton.setIcon(QIcon("img:icons/fa-bars-solid.svg"))
        self.menuButton.setIconSize(QSize(20,20))
