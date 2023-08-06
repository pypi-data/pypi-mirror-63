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
from pathlib import Path

__version__ = "0.1.2"
__info__ = {
    "name": __name__,
    "url": "https://github.com/snakypy/zshpower",
    "organization_name": "Snakypy",
    "author": {
        "name": "William Canin",
        "email": "william.costa.canin@gmail.com",
        "website": "https://williamcanin.github.io",
        "github": "https://github.com/williamcanin",
    },
    "credence": [
        {
            "my_name": "William Canin",
            "email": "william.costa.canin@gmail.com",
            "website": "http://williamcanin.me",
            "locale": "Brazil - SP",
        }
    ],
}

HOME = str(Path.home())
