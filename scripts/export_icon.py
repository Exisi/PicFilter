"""Export a PNG icon from the ICO file used by the desktop builds.

Usage: python scripts/export_icon.py doc/img/favicon.ico build/picfilter.png
"""

import sys
from pathlib import Path

from PIL import Image

ICON_SIZE = (256, 256)


def main(argv):
    if len(argv) != 3:
        print('usage: python scripts/export_icon.py <source.ico> <output.png>')
        return 1

    source = Path(argv[1])
    target = Path(argv[2])
    target.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as image:
        icon = image.convert('RGBA').resize(ICON_SIZE, Image.LANCZOS)
        icon.save(target, format='PNG')

    print('exported {}'.format(target))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
