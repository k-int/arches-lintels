import logging
import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFontDatabase

from scripts.build_ui import build_ui
from arches_lintels.settings import APP_ROOT
from arches_lintels.logging import configure_logging


def main():
    # run .ui to .py conversions
    build_ui()

    # import main window after rebuilding ui
    from arches_lintels.controllers.mainwindow import MainWindow

    configure_logging()

    app = QApplication(sys.argv)

    QDir.addSearchPath("styles", os.path.join(APP_ROOT, "styles"))
    fonts = [
        "styles:fonts/opensans/OpenSans-Regular.ttf",
        "styles:fonts/opensans/OpenSans-Light.ttf",
        "styles:fonts/opensans/OpenSans-SemiBold.ttf",
        "styles:fonts/opensans/OpenSans-Bold.ttf",
    ]
    for font in fonts:
        QFontDatabase.addApplicationFont(font)

    with open(os.path.join(APP_ROOT, "styles", "lintels.qss")) as f:
        app.setStyleSheet(f.read())

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
