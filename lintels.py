import sys
from PyQt6.QtWidgets import QApplication

from arches_lintels.controllers.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    with open("arches_lintels/resources/lintels.qss", "r") as f:
        app.setStyleSheet(f.read())    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
