import subprocess

from controls.controls_stroke import ControlsStroke
from controls.file_manipulator import FileManipulator


class ControlsStrokeSwanctlHook(ControlsStroke, FileManipulator):
    def update_hook(self):
        subprocess.run(['sudo', 'swanctl', '-sc'])  # equivalent to '--load-creds --clear'
