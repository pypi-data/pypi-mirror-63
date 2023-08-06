import tomlkit
import snakypy
from os.path import exists
from datetime import datetime
from zshpower import __version__

content = f'''# Generate by: ZSHPower - D{datetime.today().isoformat()}
# Version: {__version__}
# ---------------------------------------------------------------------
# NOTE: If you edit this file outside of "snakypy-prompt config --open",
# run the "snakypy-prompt reload" command for the changes to take effect.

[general]
separator = ""
negative.enable = false

[username]
enable = true
color = "cyan"
root.suffix = "in"

[hostname]
enable = true
color = "magenta"
prefix.color = "green"
prefix.text = "at"

[path]
color = "cyan"
involved = ""
prefix.color = "green"
prefix.text = "in"
abspath.enable = false

[git]
enable = true
branch.color = "cyan"
prefix.color = "green"
prefix.text = "on"
symbol.color = "white"

[input]
symbol = "\\uf553"
color = "green"

[pyproject]
enable = true
color = "magenta"
prefix.color = "green"
prefix.text = "on"

[python]
color = "yellow"
prefix.color = "green"
prefix.text = "via"
version.enable = true
version.minor.enable = true
version.micro.enable = true

[ssh]
color = "magenta"
prefix.color = "green"
prefix.text = "via"
info.enable = true
userhost.enable = true

[virtualenv]
enable = true
style = "normal"
text = "venv"
color = "yellow"
prefix.color = "green"
prefix.text = "via"
'''


def create(file_path, force=False):
    if not exists(file_path) or force:
        parsed_toml = tomlkit.parse(content)
        write_toml = tomlkit.dumps(parsed_toml)
        snakypy.file.create(write_toml, file_path, force=force)
        return True
    return
