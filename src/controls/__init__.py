from .controls_abstract import Controls
from .controls_stroke import ControlsStroke

controls: Controls = ControlsStroke()

__all__ = [
    'controls',
]
