"""User preference persistence for the application settings file."""

import json
import os
import tempfile


def _settings_path():
    base = os.environ.get('APPDATA') or tempfile.gettempdir()
    return os.path.join(base, 'PicFilter', 'settings.json')


def load():
    try:
        with open(_settings_path(), encoding='utf-8') as source:
            settings = json.load(source)
    except (OSError, ValueError):
        return {}
    return settings if isinstance(settings, dict) else {}


def save(key, value):
    settings = load()
    settings[key] = value
    path = _settings_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as target:
            json.dump(settings, target, ensure_ascii=False, indent=2)
    except OSError:
        pass
