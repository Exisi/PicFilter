"""Runtime translation support for the Chinese and English interface."""

import ctypes
import json
import locale
import os
import sys

from . import Settings

DEFAULT_LANGUAGE = 'en'
LANGUAGE_LABELS = {'zh': '中文', 'en': 'English'}
LANGUAGE_DIR = 'languages'

TYPE_FOLDER_KEYS = {
    0: 'folder.square',
    1: 'folder.horizontal',
    2: 'folder.vertical',
}

_current = DEFAULT_LANGUAGE


def _resource_dir():
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_table(language):
    path = os.path.join(_resource_dir(), LANGUAGE_DIR, f'{language}.json')
    try:
        with open(path, encoding='utf-8') as source:
            table = json.load(source)
    except (OSError, ValueError):
        return {}
    return table if isinstance(table, dict) else {}


TRANSLATIONS = {language: _load_table(language) for language in LANGUAGE_LABELS}


def detect_system_language():
    if sys.platform == 'win32':
        try:
            language_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        except (AttributeError, OSError):
            pass
        else:
            return 'zh' if (language_id & 0x3FF) == 0x04 else DEFAULT_LANGUAGE
    try:
        name = locale.getlocale()[0] or ''
    except ValueError:
        name = ''
    return 'zh' if name.lower().startswith('zh') else DEFAULT_LANGUAGE


def load_language():
    global _current
    language = Settings.load().get('language')
    if language in TRANSLATIONS:
        _current = language
    else:
        _current = detect_system_language()
    return _current


def save_language(language):
    Settings.save('language', language)


def set_language(language):
    global _current
    if language in TRANSLATIONS:
        _current = language


def get_language():
    return _current


def tr(key, **values):
    table = TRANSLATIONS.get(_current, {})
    text = table.get(key) or TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(key) or key
    if not values:
        return text
    try:
        return text.format(**values)
    except (KeyError, IndexError):
        return text


def type_folder(index):
    return tr(TYPE_FOLDER_KEYS.get(index, 'folder.square'))
