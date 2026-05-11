import sys
from PyQt6.QtWidgets import QApplication

from scripts.build_ui import build_ui

from arches_lintels.controllers.mainwindow import MainWindow

from arches_lintels.models.settings_model import SettingsModel


def main():
    # run .ui to .py conversions
    build_ui()

    app = QApplication(sys.argv)
    with open("arches_lintels/styles/lintels.qss", "r") as f:
        app.setStyleSheet(f.read())    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
