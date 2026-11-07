"""Runtime translation support for the Chinese and English interface."""

import json
import os
import sys
import tempfile

DEFAULT_LANGUAGE = 'zh'
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


def _settings_path():
    base = os.environ.get('APPDATA') or tempfile.gettempdir()
    return os.path.join(base, 'PicFilter', 'settings.json')


def load_language():
    global _current
    try:
        with open(_settings_path(), encoding='utf-8') as settings:
            language = json.load(settings).get('language')
    except (OSError, ValueError, AttributeError):
        language = None
    if language in TRANSLATIONS:
        _current = language
    return _current


def save_language(language):
    path = _settings_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        settings = {}
        try:
            with open(path, encoding='utf-8') as current:
                settings = json.load(current)
            if not isinstance(settings, dict):
                settings = {}
        except (OSError, ValueError):
            settings = {}
        settings['language'] = language
        with open(path, 'w', encoding='utf-8') as target:
            json.dump(settings, target, ensure_ascii=False, indent=2)
    except OSError:
        pass


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
