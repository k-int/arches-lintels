from PyQt6.QtWidgets import QMainWindow, QApplication

from arches_lintels.views.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Lintels Main Window interface class
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.is_fullscreen = True
