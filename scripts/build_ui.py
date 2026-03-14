import subprocess
import os
from pathlib import Path  

def build_ui():
    ui_dir = Path("./arches_lintels/ui/")
    views_dir = Path("./arches_lintels/views/")

    for ui_file in ui_dir.glob('*.ui'):
        file_name = ui_file.stem
        python_file = f"{file_name}.py"
        python_file_path = Path(views_dir, python_file)

        print(ui_file, python_file_path)

        command = ['pyuic6', ui_file, '-o', python_file_path]
        subprocess.call(command, shell=True)