import os

from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import QDir, QSize, Qt
from PyQt6.QtWidgets import QMainWindow

from arches_lintels.settings import APP_ROOT, VERSION
from arches_lintels.views.ui_mainwindow import Ui_MainWindow
from arches_lintels.controllers.settings_page import SettingsPage
from arches_lintels.controllers.control_centre_page import ControlCentreController
from arches_lintels.controllers.arches_manager import ArchesManagerController


class MainWindow(QMainWindow):
    """
    Lintels Main Window interface class
    """

    def __init__(self, settings_model):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

        # controllers for individual pages
        self.settings_controller = SettingsPage(self.ui, settings_model)
        self.control_centre_controller = ControlCentreController(self.ui, settings_model)
        self.arches_manager_controller = ArchesManagerController(self.ui, settings_model)

    def init_ui(self):
        QDir.addSearchPath("img", os.path.join(APP_ROOT, "img"))

        self.ui.homeButtonIconOnly.setIcon(
            QIcon("img:icons/fa-archway-solid-white.svg")
        )
        self.ui.homeButtonIconOnly.setIconSize(QSize(20, 20))
        self.ui.homeFull.setIcon(QIcon("img:icons/fa-archway-solid-white.svg"))
        self.ui.homeFull.setIconSize(QSize(20, 20))

        self.ui.controlCentreIconOnly.setIcon(
            QIcon("img:icons/fa-bars-progress-solid-white.svg")
        )
        self.ui.controlCentreIconOnly.setIconSize(QSize(20, 20))
        self.ui.controlCentreFull.setIcon(
            QIcon("img:icons/fa-bars-progress-solid-white.svg")
        )
        self.ui.controlCentreFull.setIconSize(QSize(20, 20))

        self.ui.archesCentreIconOnly.setIcon(QIcon("img:Arches_icon_white.svg"))
        self.ui.archesCentreIconOnly.setIconSize(QSize(20, 20))
        self.ui.archesCentreFull.setIcon(QIcon("img:Arches_icon_white.svg"))
        self.ui.archesCentreFull.setIconSize(QSize(20, 20))

        self.ui.settingsIconOnly.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))
        self.ui.settingsIconOnly.setIconSize(QSize(20, 20))
        self.ui.settingsFull.setIcon(QIcon("img:icons/fa-gear-solid-white.svg"))
        self.ui.settingsFull.setIconSize(QSize(20, 20))

        self.ui.aboutIconOnly.setIcon(
            QIcon("img:icons/fa-circle-question-regular-white.svg")
        )
        self.ui.aboutIconOnly.setIconSize(QSize(20, 20))
        self.ui.aboutFull.setIcon(
            QIcon("img:icons/fa-circle-question-regular-white.svg")
        )
        self.ui.aboutFull.setIconSize(QSize(20, 20))

        self.ui.menuButton.setIcon(QIcon("img:icons/fa-bars-solid.svg"))
        self.ui.menuButton.setIconSize(QSize(20, 20))

        self.ui.versionIconOnly.setText(VERSION)
        self.ui.versionFull.setText(f"Lintels {VERSION}")

        self.ui.logoIconOnly.setText("")
        self.ui.logoIconOnly.setPixmap(
            QPixmap("img:lintels-logo.svg").scaled(
                46,
                46,
                # Qt.AspectRatioMode.KeepAspectRatio,
                # Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.ui.logoIconFull.setText("")
        self.ui.logoIconFull.setPixmap(
            QPixmap("img:lintels-logo.svg").scaled(
                46,
                46,
                # Qt.AspectRatioMode.KeepAspectRatio,
                # Qt.TransformationMode.SmoothTransformation,
            )
        )

        # initialise full menu visible by default
        self.ui.iconOnlyMenu.setVisible(False)
        self.ui.fullMenu.setVisible(True)
        self.ui.menuButton.clicked.connect(self.navbar_menu_btn_change)

        # Needs to change index for both full and collapsed navbar
        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.homeButtonIconOnly.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )
        self.ui.homeFull.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )

        self.ui.controlCentreIconOnly.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1)
        )
        self.ui.controlCentreFull.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1)
        )

        self.ui.archesCentreIconOnly.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(2)
        )
        self.ui.archesCentreFull.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(2)
        )

        self.ui.settingsIconOnly.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(3)
        )
        self.ui.settingsFull.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(3)
        )

        self.ui.aboutIconOnly.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(4)
        )
        self.ui.aboutFull.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(4)
        )

    def navbar_menu_btn_change(self):
        if self.ui.menuButton.isChecked():
            self.ui.iconOnlyMenu.setVisible(True)
            self.ui.fullMenu.setVisible(False)
        else:
            self.ui.iconOnlyMenu.setVisible(False)
            self.ui.fullMenu.setVisible(True)
