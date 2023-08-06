from tomlkit import parse
import snakypy
from os.path import join


def template_preferences(config_root_folder):
    config_load = snakypy.file.read(join(config_root_folder, 'config.toml'))
    parsed = parse(config_load)

    data = {'preferences.zsh': f'''#!/usr/bin/env bash
SNAKYPY__SEPARATOR="{parsed['general']['separator']}"
SNAKYPY__USERNAME_COLOR="{parsed['username']['color']}"
SNAKYPY__HOSTNAME_COLOR="{parsed['hostname']['color']}"
SNAKYPY__HOSTNAME_PREFIX_COLOR="{parsed['hostname']['prefix']['color']}"
SNAKYPY__PATH_DIR_PREFIX_COLOR="{parsed['path']['prefix']['color']}"
SNAKYPY__PATH_FOLDER_COLOR="{parsed['path']['color']}"
SNAKYPY__GIT_PREFIX_COLOR="{parsed['git']['prefix']['color']}"
SNAKYPY__GIT_BRANCH_COLOR="{parsed['git']['branch']['color']}"
SNAKYPY__GIT_ICON_COLOR="{parsed['git']['symbol']['color']}"
SNAKYPY__INPUT_COLOR="{parsed['input']['color']}"
SNAKYPY__PYTHON_COLOR="{parsed['python']['color']}"
SNAKYPY__PYTHON_PREFIX_COLOR="{parsed['python']['prefix']['color']}"
SNAKYPY__VIRTUALENV_COLOR="{parsed['virtualenv']['color']}"
SNAKYPY__VIRTUALENV_PREFIX_COLOR="{parsed['virtualenv']['prefix']['color']}"
SNAKYPY__SSH_COLOR="{parsed['ssh']['color']}"
SNAKYPY__SSH_PREFIX_COLOR="{parsed['ssh']['prefix']['color']}"
SNAKYPY__PYPROJECT_COLOR="{parsed['pyproject']['color']}"
SNAKYPY__PYPROJECT_PREFIX_COLOR="{parsed['pyproject']['prefix']['color']}"
SNAKYPY__PY_VERSION_PREFIX_TEXT="{parsed['python']['prefix']['text']}"
SNAKYPY__VIRTUALENV_PREFIX_TEXT="{parsed['virtualenv']['prefix']['text']}"
SNAKYPY__SSH_PREFIX_TEXT="{parsed['ssh']['prefix']['text']}"
SNAKYPY__VIRTUALENV_TEXT="{parsed['virtualenv']['text']}"
SNAKYPY__HOSTNAME_PREFIX_TEXT="{parsed['hostname']['prefix']['text']}"
SNAKYPY__GIT_PREFIX_TEXT="{parsed['git']['prefix']['text']}"
SNAKYPY__USERNAME_SUFFIX_ROOT_TEXT="{parsed['username']['root']['suffix']}"
SNAKYPY__PYPROJECT_PREFIX_TEXT="{parsed['pyproject']['prefix']['text']}"
SNAKYPY__PATH_DIR_PREFIX_TEXT="{parsed['path']['prefix']['text']}"
SNAKYPY__INPUT_PROMPT_SYMBOL="{parsed['input']['symbol']}"
SNAKYPY__VIRTUALENV_STYLE="{parsed['virtualenv']['style']}"
SNAKYPY__PATH_FOLDER_INVOLVED="{parsed['path']['involved']}"
SNAKYPY__NEGATIVE_COLOR_ENABLE={parsed['general']['negative']['enable']}
SNAKYPY__GIT_ENABLE={parsed['git']['enable']}
SNAKYPY__PY_VERSION_ENABLE={parsed['python']['version']['enable']}
SNAKYPY__PY_VERSION_MINOR_ENABLE={parsed['python']['version']['minor']['enable']}
SNAKYPY__PY_VERSION_MICRO_ENABLE={parsed['python']['version']['micro']['enable']}
SNAKYPY__VIRTUALENV_ENABLE={parsed['virtualenv']['enable']}
SNAKYPY__USERNAME_ENABLE={parsed['username']['enable']}
SNAKYPY__HOSTNAME_ENABLE={parsed['hostname']['enable']}
SNAKYPY__SSH_INFO_ENABLE={parsed['ssh']['info']['enable']}
SNAKYPY__ENABLE_HOSTNAME_USERNAME_SSH={parsed['ssh']['userhost']['enable']}
SNAKYPY__ABSOLUTE_PATH_ENABLE={parsed['path']['abspath']['enable']}
SNAKYPY__PYPROJECT_ENABLE={parsed['pyproject']['enable']}
'''}
    return data
