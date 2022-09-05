from .controls_abstract import Controls
from .controls_stroke_swanctl_hook import ControlsStrokeSwanctlHook

controls: Controls = ControlsStrokeSwanctlHook()

__all__ = [
    'controls',
]
