import os

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QDir, QSize, Qt

from arches_lintels.settings import APP_ROOT
from arches_lintels.controllers.utils.update_widget_styling import update_widget_styling


class DependencyUIUpdates:
    def __init__(
        self, install_label, install_button, start_button, stop_button, running_label
    ):
        self.install_label = install_label
        self.install_button = install_button
        self.start_button = start_button
        self.stop_button = stop_button
        self.running_label = running_label

        QDir.addSearchPath("img", os.path.join(APP_ROOT, "img"))
        # Using QPixmap here because we're setting on a label rather than a button
        self.green_tick = QPixmap("img:icons/fa-circle-check-solid-green.svg").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.red_cross = QPixmap("img:icons/fa-circle-xmark-solid-red.svg").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    def default_installed(self):
        self.install_label.setText("")
        self.install_label.setPixmap(self.green_tick)
        update_widget_styling(self.install_label, "state", "installed")
        self.install_button.setEnabled(False)
        self.install_button.hide()
        self.start_button.show()
        self.start_button.setEnabled(True)
        self.running_label.setText("")
        self.running_label.setPixmap(self.red_cross)
        update_widget_styling(self.running_label, "state", "not_running")
        self.stop_button.setEnabled(False)
        self.stop_button.hide()

    def default_not_installed(self):
        self.install_label.setText("")
        self.install_label.setPixmap(self.red_cross)
        self.install_button.show()
        self.install_button.setText("Install")
        update_widget_styling(self.install_label, "state", "not_installed")
        # If not installed then also not running
        self.install_button.setEnabled(True)
        self.start_button.show()
        self.start_button.setEnabled(False)
        self.running_label.setText("")
        self.running_label.setPixmap(self.red_cross)
        update_widget_styling(self.running_label, "state", "not_running")
        self.stop_button.setEnabled(False)
        self.stop_button.hide()

    def default_running(self):
        """
        When running the start button should be hidden and the stop button visible.
        """
        update_widget_styling(self.running_label, "state", "running")
        self.running_label.setText("")
        self.running_label.setPixmap(self.green_tick)
        self.start_button.setEnabled(False)
        self.start_button.hide()
        self.stop_button.setEnabled(True)
        self.stop_button.show()

    def default_starting(self):
        """
        When starting the stop button should be visible but disabled, the start button
        should be hidden and disabled.
        """
        update_widget_styling(self.running_label, "state", "starting")
        self.running_label.setText("Starting")
        self.start_button.setEnabled(False)
        self.start_button.hide()
        self.stop_button.setEnabled(False)
        self.stop_button.show()

    def default_not_running(self):
        """
        When not running the start button should be visible and stop hidden.
        """
        update_widget_styling(self.running_label, "state", "not_running")
        self.running_label.setText("")
        self.running_label.setPixmap(self.red_cross)
        self.start_button.setEnabled(True)
        self.start_button.show()
        self.stop_button.setEnabled(False)
        self.stop_button.hide()

    def default_stopping(self):
        """
        When stopping the start button should be hidden and stop visible but disabled.
        """
        self.running_label.setText("Stopping")
        update_widget_styling(self.running_label, "state", "not_running")
        self.start_button.setEnabled(False)
        self.start_button.hide()
        self.stop_button.setEnabled(False)
        self.stop_button.show()

