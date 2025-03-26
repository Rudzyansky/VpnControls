from telegram.ext import Application

from . import registration, privileges, accounting, settings

flows = [registration, privileges, accounting, settings]


def register(application: Application):
    """Register all handlers from all flows with the application"""
    for flow in flows:
        for module in flow.modules:
            for handler in module.get_handlers():
                application.add_handler(handler)


__all__ = [
    'register'
]
