import re
import sys
import locale
import argparse
import os
import pathlib
import tzlocal
#import happylogging

import miyadaiku.core.__version__
from miyadaiku.core.site import MODULES_DIR, CONTENTS_DIR, FILES_DIR, TEMPLATES_DIR

locale.setlocale(locale.LC_ALL, '')

parser = argparse.ArgumentParser(description='Start new miyadaiku document.')
parser.add_argument('directory', help='directory name')
parser.add_argument('--version', '-v', action='version',
                    version=f'{miyadaiku.core.__version__}')


def main():
    #    happylogging.initlog(filename='-', level='DEBUG')

    args = parser.parse_args()

    d = pathlib.Path(args.directory)
    if d.exists():
        print(f'{str(d)!r} already exists', file=sys.stderr)
        sys.exit(1)

    tz = tzlocal.get_localzone().zone

    locale.setlocale(locale.LC_ALL, '')
    lang = locale.getlocale()[0]
    lang = (lang or "en-US").replace('_', '-')
    charset = "utf-8"

    yaml = f"""# Miyadaiku config file

# Base URL of the site
site_url: http://localhost:8888/

# Title of the site
site_title: FIXME - site title

# Default language code
lang: {lang}

# Default charset
charset: {charset}

# Default timezone
timezone: {tz}

# List of site theme
# themes:
#   - miyadaiku.themes.sample.blog

"""
    (d / CONTENTS_DIR).mkdir(parents=True)
    (d / MODULES_DIR).mkdir()
    (d / FILES_DIR).mkdir()
    (d / TEMPLATES_DIR).mkdir()

    (d / 'config.yml').write_text(yaml, 'utf-8')


if __name__ == '__main__':
    main()
