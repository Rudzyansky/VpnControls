from typing import Any, Dict, Optional, Protocol

from telegram.ext import ExtBot, Application
from telegram.ext._callbackcontext import CallbackContext, ST
from telegram.ext._contexttypes import ADict
from telegram.ext._utils.types import BT, UD, CD, BD

from domain import common
from .localization_manager import Localization


class ContextProto(Protocol):
    def localize(self, key: str) -> str: ...

    @property
    def chat_id(self): ...

    @property
    def user_id(self): ...


class LocalizedContext(CallbackContext[ExtBot[Any], ADict, ADict, ADict], ContextProto):
    """Custom context type that includes translation functionality"""

    def __init__(
            self: ST,
            application: Application[BT, ST, UD, CD, BD, Any],
            chat_id: Optional[int] = None,
            user_id: Optional[int] = None,
    ):
        CallbackContext.__init__(self, application, chat_id, user_id)
        self._language: Optional[str] = None
        self._translations: Optional[Dict[str, str]] = None

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def language(self) -> str:
        """Get the current language"""
        return common.language(self._user_id)

    def localize(self, key: str, lang: str = None) -> str:
        """Get a translation for the current language"""
        if lang is None:
            lang = self.language
        return Localization.get_translation(lang, key)

    @staticmethod
    def get_all_translations(key: str) -> Dict[str, str]:
        """Get translations for a key in all languages"""
        return Localization.get_all_translations(key)
