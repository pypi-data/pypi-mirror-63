import os
import snakypy
from snakypy import printer, FG
from snakypy.console import billboard, pick
from docopt import docopt
from sys import exit
from datetime import datetime
from subprocess import call
from shutil import rmtree, which, copyfile
from os.path import join, exists
from zshpower import template
from zshpower import (__version__, __name__, _PACKAGE, _omz_root_folder,
                      _zsh_rc, _template_dirs, _config_root_folder,
                      _themes_folder, _plugins)
from zshpower import (utils, console, system, omz, zshrc, config, decorators)

app_name = _PACKAGE['name'].replace('-', ' ').title()
menu_opt = f"""
{app_name} Theme Manager.

Usage:
    {_PACKAGE['name']} init
    {_PACKAGE['name']} config (--open | --view)
    {_PACKAGE['name']} reload
    {_PACKAGE['name']} enable
    {_PACKAGE['name']} disable [--theme=<name>]
    {_PACKAGE['name']} reset
    {_PACKAGE['name']} uninstall
    {_PACKAGE['name']} --help
    {_PACKAGE['name']} --version
    {_PACKAGE['name']} --credits

Arguments:
    init ---------- Install dependencies like Oh My ZSH and plugins and activate
                    the {app_name} theme.
    reload -------- If you do not use the "config --open" option and edit the settings
                    externally, use this option for the changes to take effect.
                    The configuration file is located at:
                    "{_config_root_folder}/config.toml".
    enable -------- Activate the {app_name} theme.
    disable ------- Disable the {app_name} theme and go back to the old one.
    reset --------- Reset to default settings.
    uninstall ----- Uninstall the package {app_name}.
                    NOTE: If you installed {app_name} with "sudo", use "sudo" with
                    this option as well. E.g: "sudo snakypy-prompt uninstall".
    config -------- The easiest way to edit and view the settings is through this option.

Options:
    -h --help ------ Show this screen.
    --open --------- Open the configuration file in edit mode and perform the automatic
                     update when you exit.
    --view --------- View the configuration file on the terminal.
    --theme=<name> - Get the name of a theme available on Oh My ZSH [Default: robbyrussell].
    --version ------ Show version.
    --credits ------ Show credits.

For more information, access: {_PACKAGE['url']}
"""


def arguments():
    data = docopt(menu_opt, version=__version__)
    return data


def banner():
    printer('\nOffered by:', foreground=FG.GREEN)
    billboard(_PACKAGE['organization_name'], foreground=FG.CYAN)
    printer(f'copyright (c) since 2020\n\n'.center(60), foreground=FG.GREEN)


@decorators.assign_cli(arguments, 'init')
def init():
    banner()

    system.tools_requirements('git', 'vim', 'zsh')
    snakypy.path.create(_config_root_folder)
    config.create(join(_config_root_folder, 'config.toml'))

    omz.install(_omz_root_folder)

    if exists(_omz_root_folder):
        for plugin in _plugins:
            while exists(join(_omz_root_folder, f"custom/plugins/{plugin}")):
                break
            else:
                omz.install_plugins(_omz_root_folder, _plugins)
                continue

    snakypy.path.create(multidir=_template_dirs)

    utils.generate_template(_template_dirs[0], template.template_variables())
    utils.generate_template(_template_dirs[0],
                            template.template_preferences(_config_root_folder))
    utils.generate_template(_template_dirs[1], template.template_git())
    utils.generate_template(_template_dirs[1], template.template_hostname())
    utils.generate_template(_template_dirs[1], template.template_input())
    utils.generate_template(_template_dirs[1], template.template_path())
    utils.generate_template(_template_dirs[1], template.template_prompt())
    utils.generate_template(_template_dirs[1], template.template_pyproject())
    utils.generate_template(_template_dirs[1], template.template_python())
    utils.generate_template(_template_dirs[1], template.template_ssh())
    utils.generate_template(_template_dirs[1], template.template_username())
    utils.generate_template(_template_dirs[1], template.template_virtualenv())
    utils.generate_template(_template_dirs[2], template.template_utils())
    utils.generate_template(_themes_folder, template.template_zshpower())

    system.install_fonts()
    zshrc.create(zshrc.content, _zsh_rc)
    zshrc.change_theme(_zsh_rc, 'zshpower')
    zshrc.add_plugins(_zsh_rc)
    console.change_shell()

    printer('Done! Nothing more to do.', foreground=FG.FINISH)
    console.reload_zsh()


@decorators.assign_cli(arguments, 'config')
def open_config():
    import pydoc

    if arguments()['--open']:
        editors = ['vim', 'nano', 'emacs']
        for editor in editors:
            if which(editor):
                get_editor = os.environ.get('EDITOR', editor)
                with open(join(_config_root_folder, 'config.toml')) as f:
                    call([get_editor, f.name])
                    utils.generate_template(_template_dirs[0],
                                            template.template_preferences(_config_root_folder))
                    printer('Done!', foreground=FG.FINISH)
                    console.reload_zsh()
                return True
        return

    if arguments()['--view']:
        read_config = snakypy.file.read(join(_config_root_folder, 'config.toml'))
        pydoc.pager(read_config)


@decorators.checking_init(_themes_folder)
@decorators.assign_cli(arguments, 'enable')
def enable():
    if zshrc.read(_zsh_rc)[0] == 'zshpower':
        printer('Already enabled. Nothing to do.', foreground=FG.FINISH)
        exit(0)
    zshrc.change_theme(_zsh_rc, 'zshpower')
    printer('Done!', foreground=FG.FINISH)
    console.reload_zsh()


@decorators.assign_cli(arguments, 'disable')
def disable(*, theme_name='robbyrussell'):
    if not zshrc.read(_zsh_rc)[0] == 'zshpower':
        printer('Already disabled. Nothing to do.', foreground=FG.FINISH)
        exit(0)
    if not arguments()['--theme']:
        zshrc.change_theme(_zsh_rc, theme_name)
    else:
        zshrc.change_theme(_zsh_rc, arguments()['--theme'])
    printer('Done!', foreground=FG.FINISH)
    console.reload_zsh()


@decorators.assign_cli(arguments, '--credits')
def credence():
    snakypy.console.credence(app_name, __version__, _PACKAGE['url'],
                             _PACKAGE, foreground=FG.CYAN)


@decorators.assign_cli(arguments, 'reload')
def reload_config():
    utils.generate_template(_template_dirs[0],
                            template.template_preferences(_config_root_folder))
    printer('Done!', foreground=FG.FINISH)
    console.reload_zsh()


@decorators.assign_cli(arguments, 'reset')
def reset_config():
    config.create(join(_config_root_folder, 'config.toml'), force=True)
    utils.generate_template(_template_dirs[0],
                            template.template_preferences(_config_root_folder))
    printer('Done!', foreground=FG.FINISH)
    console.reload_zsh()


@decorators.assign_cli(arguments, 'uninstall')
def uninstall():
    from sys import exit
    from contextlib import suppress
    from subprocess import check_output

    banner()

    title = f'What did you want to uninstall?'
    options = [f'Only {app_name}', f'{app_name} and Oh My ZSH', 'None']
    reply = pick(title, options, colorful=True, index=True)

    if reply is None or reply[0] == 2:
        printer('Whew! Thanks! :)', foreground=FG.GREEN)
        exit(0)

    with suppress(Exception):
        os.remove(join(_themes_folder, ''.join(template.template_zshpower().keys())))
    rmtree(join(_themes_folder, __name__), ignore_errors=True)
    # # Do not remove settings on uninstall.
    # # If you want to remove, uncomment the line below.
    # rmtree(_config_root_folder, ignore_errors=True)

    pip_check = which('pip')
    if pip_check is not None:
        check_output(f'pip uninstall {_PACKAGE["name"]} -y',
                     shell=True, universal_newlines=True)
    zshrc.change_theme(_zsh_rc, 'robbyrussell')

    if reply[0] == 1:
        rmtree(_omz_root_folder, ignore_errors=True)
        with suppress(Exception):
            copyfile(_zsh_rc, f'{_zsh_rc}-D{datetime.today().isoformat()}')
        with suppress(Exception):
            os.remove(_zsh_rc)

    console.reload_zsh()

    printer('Uninstall process finished.', foreground=FG.FINISH)


@snakypy.decorators.use_unix_system
def main():
    init()
    enable()
    disable()
    credence()
    uninstall()
    open_config()
    reset_config()
    reload_config()
