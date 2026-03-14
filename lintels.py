import sys
from PyQt6.QtWidgets import QApplication

from scripts.build_ui import build_ui



def main():
    # run .ui to .py conversions
    build_ui()

    from arches_lintels.controllers.mainwindow import MainWindow

    app = QApplication(sys.argv)
    with open("arches_lintels/resources/lintels.qss", "r") as f:
        app.setStyleSheet(f.read())    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
