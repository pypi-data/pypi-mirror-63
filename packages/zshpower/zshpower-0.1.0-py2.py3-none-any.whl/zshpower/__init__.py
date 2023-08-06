"""
ZSHPower
~~~~~~~~

ZSHPower is a theme for Oh My Zsh framework; especially
for the Python developer. Pleasant to look at, the ZSHPower
comforts you with its colors and icons vibrant.

For more information, access: https://github.com/snakypy/zshpower

:copyright: Copyright 2020-2020 by Snakypy team, see AUTHORS.
:license: MIT, see LICENSE for details.

"""

from . import __name__
from os.path import join
from pathlib import Path

__version__ = '0.1.0'

_PACKAGE = {
    'name': __name__,
    'url': 'https://github.com/snakypy/zshpower',
    'organization_name': 'Snakypy',
    'author': {
        'name': 'William Canin',
        'email': 'william.costa.canin@gmail.com',
        'website': 'https://williamcanin.github.io',
        'github': 'https://github.com/williamcanin'
    },
    'credence': [{
        'my_name': 'William Canin',
        'email': 'william.costa.canin@gmail.com',
        'website': 'http://williamcanin.me',
        'locale': 'Brazil - SP'
    }]
}

_HOME = str(Path.home())
_omz_root_folder = join(_HOME, '.oh-my-zsh')
_config_root_folder = join(_HOME, f'.config/snakypy/zshpower/{__version__}')
_themes_folder = join(_omz_root_folder, 'custom/themes')
_zsh_rc = join(_HOME, '.zshrc')
_plugins = ['zsh-syntax-highlighting', 'zsh-autosuggestions']
_template_dirs = (join(_themes_folder, f'{__name__}'),
                  join(_themes_folder, f'{__name__}/sections'),
                  join(_themes_folder, f'{__name__}/lib'))
