from PyQt6.QtWidgets import QFileDialog

def file_browser(title="Select install folder", dir_only=False):
    file_dialog = QFileDialog()
    file_dialog.setWindowTitle(title)

    if dir_only:
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
    else:
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

    file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()      
        # return single file
        return selected_files[0]