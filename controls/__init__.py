from .controlsabstract import Controls
from .controlsstroke import StrokeControls

controls = StrokeControls()

add_user = controls.add_user
remove_user = controls.remove_user
reset_password = controls.reset_password
change_username = controls.change_username

__all__ = [
    'add_user',
    'remove_user',
    'reset_password',
    'change_username'
]
