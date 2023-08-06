import os
import snakypy
from zshpower import _HOME, _PACKAGE
from snakypy import printer, FG
from shutil import which
from sys import platform
from os.path import join, exists
from zipfile import ZipFile


def tools_requirements(*args):
    for tool in args:
        if which(tool) is None:
            raise Exception(f'The package \'{_PACKAGE["name"]}\' needs the "{tool}" tool. '
                            'Tool not found. Aborted.')


def install_fonts(force=False):
    url = 'https://github.com/snakypy/snakypy-static'
    base_url = f'blob/master/zshpower/fonts/fonts.zip?raw=true'
    font_name = 'DejaVu Sans Mono Nerd Font'
    fonts_dir = join(_HOME, f'.fonts')
    snakypy.path.create(fonts_dir)
    curl_output = join(_HOME, "zshpower__font.zip")

    if platform.startswith('linux'):
        try:
            if not exists(join(fonts_dir, "DejaVu Sans Mono Nerd Font Complete.ttf")) or force:
                printer(f'Please wait, downloading the "{font_name}" font and installing...',
                        foreground=FG.QUESTION)
                cmd_line = f'curl -L {join(url, base_url)} --output {curl_output}'
                snakypy.console.cmd(cmd_line, verbose=True)

                with ZipFile(curl_output, 'r') as zip_ref:
                    zip_ref.extractall(fonts_dir)
                    os.remove(curl_output)
                    printer('Done!', foreground=FG.FINISH)
                return True
            return
        except Exception as err:
            raise Exception(f'Error downloading font "{font_name}"', err)
    return
