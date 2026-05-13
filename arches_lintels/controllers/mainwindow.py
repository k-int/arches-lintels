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

        self.settings = SettingsModel()
        self.init_ui()

    def navbar_menu_btn_change(self):
        if self.menuButton.isChecked():
            self.iconOnlyMenu.setVisible(True)
            self.fullMenu.setVisible(False)
        else:
            self.iconOnlyMenu.setVisible(False)
            self.fullMenu.setVisible(True)

    def page_navigation(self):
        self.stackedWidget.setCurrentIndex(0)

        # Needs to change index for both full and collapsed navbar
        self.homeButtonIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.homeFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        
        self.controlCentreIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.controlCentreFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        
        self.archesCentreIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        self.archesCentreFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        
        self.settingsIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(3))
        self.settingsFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(3))

        self.aboutIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))
        self.aboutFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))

    def init_ui(self):
        QDir.addSearchPath("img", os.path.join(self.settings.app_root, "img"))

        self.homeButtonIconOnly.setIcon(QIcon("img:icons/fa-archway-solid-white.svg"))
        self.homeButtonIconOnly.setIconSize(QSize(20,20))
        self.homeFull.setIcon(QIcon("img:icons/fa-archway-solid-white.svg"))
        self.homeFull.setIconSize(QSize(20,20))

        self.controlCentreIconOnly.setIcon(QIcon("img:icons/fa-bars-progress-solid-white.svg"))
        self.controlCentreIconOnly.setIconSize(QSize(20,20))
        self.controlCentreFull.setIcon(QIcon("img:icons/fa-bars-progress-solid-white.svg"))
        self.controlCentreFull.setIconSize(QSize(20,20))

        self.archesCentreIconOnly.setIcon(QIcon("img:Arches_icon_white.svg"))
        self.archesCentreIconOnly.setIconSize(QSize(20,20))
        self.archesCentreFull.setIcon(QIcon("img:Arches_icon_white.svg"))
        self.archesCentreFull.setIconSize(QSize(20,20))

        self.settingsIconOnly.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))
        self.settingsIconOnly.setIconSize(QSize(20,20))
        self.settingsFull.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))
        self.settingsFull.setIconSize(QSize(20,20))

        self.aboutIconOnly.setIcon(QIcon("img:icons/fa-circle-question-regular-white.svg"))
        self.aboutIconOnly.setIconSize(QSize(20,20))
        self.aboutFull.setIcon(QIcon("img:icons/fa-circle-question-regular-white.svg"))
        self.aboutFull.setIconSize(QSize(20,20))

        self.menuButton.setIcon(QIcon("img:icons/fa-bars-solid.svg"))
        self.menuButton.setIconSize(QSize(20,20))

        # initialise full menu visible by default
        self.iconOnlyMenu.setVisible(False)
        self.fullMenu.setVisible(True)
        self.menuButton.clicked.connect(self.navbar_menu_btn_change)

        # Needs to change index for both full and collapsed navbar
        self.homeButtonIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.homeFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        
        self.controlCentreIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.controlCentreFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        
        self.archesCentreIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        self.archesCentreFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        
        self.settingsIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(3))
        self.settingsFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(3))

        self.aboutIconOnly.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))
        self.aboutFull.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))

        # set starting interface
        if not self.settings.settings_data["install_directory"]:
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.stackedWidget.setCurrentIndex(0)
