"""Sync the release version into package.json.

Usage: python scripts/set_version.py v1.2.3
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / 'package.json'
SEMVER = re.compile(r'^v?(\d+\.\d+\.\d+)$')


def main(argv):
    if len(argv) != 2:
        print('usage: python scripts/set_version.py v<major>.<minor>.<patch>')
        return 1

    match = SEMVER.match(argv[1].strip())
    if match is None:
        print('invalid version: {}'.format(argv[1]))
        return 1

    version = match.group(1)
    manifest = json.loads(PACKAGE.read_text(encoding='utf-8'))
    manifest['version'] = version
    PACKAGE.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print('package.json version -> {}'.format(version))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
