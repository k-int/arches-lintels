import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFontDatabase

from scripts.build_ui import build_ui
from arches_lintels.controllers.mainwindow import MainWindow
from arches_lintels.models.settings_model import SettingsModel


def main():
    # run .ui to .py conversions
    build_ui()

    app = QApplication(sys.argv)

    settings = SettingsModel()

    QDir.addSearchPath("styles", os.path.join(settings.app_root, "styles"))
    fonts = [
        "styles:fonts/opensans/OpenSans-Regular.ttf",
        "styles:fonts/opensans/OpenSans-Light.ttf",
        "styles:fonts/opensans/OpenSans-SemiBold.ttf",
        "styles:fonts/opensans/OpenSans-Bold.ttf",
    ]
    for font in fonts:
        QFontDatabase.addApplicationFont(font)

    with open(os.path.join(settings.app_root, "styles", "lintels.qss")) as f:
        app.setStyleSheet(f.read())

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
