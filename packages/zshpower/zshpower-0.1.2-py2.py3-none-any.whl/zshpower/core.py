import snakypy
import pydoc
import subprocess
import shutil
import os
from os.path import join, exists
from sys import exit
from datetime import datetime
from contextlib import suppress
from docopt import docopt
from snakypy import printer, FG, pick
from snakypy.ansi import NONE
from zshpower import __version__, __info__, HOME
from zshpower import utils, config, template


def show_billboard():
    printer("\nOffered by:", foreground=FG.GREEN)
    snakypy.console.billboard(__info__["organization_name"], foreground=FG.CYAN)
    printer(f"copyright (c) since 2020\n\n".center(60), foreground=FG.GREEN)


class ZSHPower:
    def __init__(self):
        self.app_name = f"{__info__['name'][:4].upper()}{__info__['name'][4:]}"
        self.omz_root_folder = join(HOME, ".oh-my-zsh")
        self.config_root_folder = join(HOME, f".config/snakypy/zshpower/{__version__}")
        self.themes_folder = join(self.omz_root_folder, "custom/themes")
        self.zsh_rc = join(HOME, ".zshrc")
        self.plugins = ["zsh-syntax-highlighting", "zsh-autosuggestions"]
        self.template_dirs = (
            join(self.themes_folder, f"{__info__['name']}"),
            join(self.themes_folder, f"{__info__['name']}/sections"),
            join(self.themes_folder, f"{__info__['name']}/lib"),
        )

    def menu(self):
        opts = f"""

{FG.MAGENTA}Welcome to the {self.app_name} options menu.{NONE}

Usage:
    {__info__['name']} init
    {__info__['name']} config (--open | --view)
    {__info__['name']} reload
    {__info__['name']} enable
    {__info__['name']} disable [--theme=<name>]
    {__info__['name']} reset
    {__info__['name']} uninstall
    {__info__['name']} --help
    {__info__['name']} --version
    {__info__['name']} --credits

Arguments:
    {FG.CYAN}init{NONE} ---------- Install dependencies like \
{FG.MAGENTA}Oh My ZSH{FG.GREEN} and plugins and activate
                    the {self.app_name} theme.
    {FG.CYAN}reload{NONE} -------- If you do not use the \
{FG.GREEN}config --open{NONE} option and edit the settings
                    externally, use this option for the changes to take effect.
                    The configuration file is located at:
                    {FG.GREEN}{self.config_root_folder}/config.toml{NONE}.
    {FG.CYAN}enable{NONE} -------- Activate the {self.app_name} theme.
    {FG.CYAN}disable{NONE} ------- Disable the {self.app_name} theme and go back \
to the default.
    {FG.CYAN}reset{NONE} --------- Reset to default settings.
    {FG.CYAN}uninstall{NONE} ----- Uninstall the package {self.app_name}.
                    {FG.YELLOW}NOTE:{NONE} If you installed {self.app_name} \
with "sudo", use "sudo" with
                    this option as well. {FG.YELLOW}E.g:{NONE} \
{FG.GREEN}sudo {__info__['name']} uninstall{NONE}.
    {FG.CYAN}config{NONE} -------- The easiest way to edit and view the \
settings is through this option.

Options:
    {FG.CYAN}--help{NONE} --------- Show this screen.
    {FG.CYAN}--open{NONE} --------- Open the configuration file in edit mode \
and perform the automatic
                     update when you exit.
    {FG.CYAN}--view{NONE} --------- View the configuration file on the \
terminal.
    {FG.CYAN}--theme=<name>{NONE} - Get the name of a theme available on \
{FG.MAGENTA}Oh My ZSH{NONE} \
[Default: {FG.GREEN}robbyrussell{NONE}].
    {FG.CYAN}--version{NONE} ------ Show version.
    {FG.CYAN}--credits{NONE} ------ Show credits.

{FG.WARNING}For more information, access: {FG.BLUE}{__info__['url']}{NONE}
        """
        return opts

    def arguments(self):
        formatted_version = f"{self.app_name} version: {FG.CYAN}{__version__}{NONE}"
        data = docopt(self.menu(), version=formatted_version)
        return data

    def init_command(self):
        show_billboard()

        utils.tools_requirements("git", "vim", "zsh")
        snakypy.path.create(self.config_root_folder)
        utils.create_config(
            config.config_content(), join(self.config_root_folder, "config.toml")
        )

        utils.omz_install(self.omz_root_folder)

        if exists(self.omz_root_folder):
            for plugin in self.plugins:
                while exists(join(self.omz_root_folder, f"custom/plugins/{plugin}")):
                    break
                else:
                    utils.omz_install_plugins(self.omz_root_folder, self.plugins)
                    continue

        snakypy.path.create(multidir=self.template_dirs)

        utils.generate_template(self.template_dirs[0], template.template_variables())
        utils.generate_template(
            self.template_dirs[0],
            template.template_preferences(self.config_root_folder),
        )

        utils.generate_template(self.template_dirs[1], template.template_git())
        utils.generate_template(self.template_dirs[1], template.template_hostname())
        utils.generate_template(self.template_dirs[1], template.template_input())
        utils.generate_template(self.template_dirs[1], template.template_path())
        utils.generate_template(self.template_dirs[1], template.template_prompt())
        utils.generate_template(self.template_dirs[1], template.template_pyproject())
        utils.generate_template(self.template_dirs[1], template.template_python())
        utils.generate_template(self.template_dirs[1], template.template_ssh())
        utils.generate_template(self.template_dirs[1], template.template_username())
        utils.generate_template(self.template_dirs[1], template.template_virtualenv())
        utils.generate_template(self.template_dirs[2], template.template_utils())
        utils.generate_template(self.themes_folder, template.template_zshpower())

        utils.install_fonts()
        utils.create_zshrc(config.zshrc_content(self.omz_root_folder), self.zsh_rc)
        utils.change_theme_in_zshrc(self.zsh_rc, "zshpower")
        utils.add_plugins_zshrc(self.zsh_rc)
        utils.change_shell()

        printer("Done! Nothing more to do.", foreground=FG.FINISH)
        utils.reload_zsh()

    def config_command(self):
        if self.arguments()["--open"]:
            editors = ("vim", "nano", "emacs")
            for editor in editors:
                if shutil.which(editor):
                    get_editor = os.environ.get("EDITOR", editor)
                    with open(join(self.config_root_folder, "config.toml")) as f:
                        subprocess.call([get_editor, f.name])
                        utils.generate_template(
                            self.template_dirs[0],
                            template.template_preferences(self.config_root_folder),
                        )
                        printer("Done!", foreground=FG.FINISH)
                        utils.reload_zsh()
                    return True
        elif self.arguments()["--view"]:
            read_config = snakypy.file.read(
                join(self.config_root_folder, "config.toml")
            )
            pydoc.pager(read_config)
            return True

    def enable_command(self):
        if utils.read_zshrc(self.zsh_rc)[0] == "zshpower":
            printer("Already enabled. Nothing to do.", foreground=FG.FINISH)
            exit(0)
        utils.change_theme_in_zshrc(self.zsh_rc, "zshpower")
        printer("Done!", foreground=FG.FINISH)
        utils.reload_zsh()

    def disable_command(self, arguments, *, theme_name="robbyrussell"):
        if not utils.read_zshrc(self.zsh_rc)[0] == "zshpower":
            printer("Already disabled. Nothing to do.", foreground=FG.FINISH)
            exit(0)
        if not arguments()["--theme"]:
            utils.change_theme_in_zshrc(self.zsh_rc, theme_name)
        else:
            utils.change_theme_in_zshrc(self.zsh_rc, arguments()["--theme"])
        printer("Done!", foreground=FG.FINISH)
        utils.reload_zsh()

    def credence_command(self):
        snakypy.console.credence(
            self.app_name, __version__, __info__["url"], __info__, foreground=FG.CYAN
        )

    def reload_command(self):
        utils.generate_template(
            self.template_dirs[0],
            template.template_preferences(self.config_root_folder),
        )
        printer("Done!", foreground=FG.FINISH)
        utils.reload_zsh()

    def reset_command(self):
        utils.create_config(
            config.config_content(),
            join(self.config_root_folder, "config.toml"),
            force=True,
        )
        utils.generate_template(
            self.template_dirs[0],
            template.template_preferences(self.config_root_folder),
        )
        printer("Done!", foreground=FG.FINISH)
        utils.reload_zsh()

    def uninstall_command(self):
        show_billboard()
        title = f"What did you want to uninstall?"
        options = [f"Only {self.app_name}", f"{self.app_name} and Oh My ZSH", "None"]
        reply = pick(title, options, colorful=True, index=True)

        if reply is None or reply[0] == 2:
            printer("Whew! Thanks! :)", foreground=FG.GREEN)
            exit(0)

        with suppress(Exception):
            os.remove(
                join(self.themes_folder, "".join(template.template_zshpower().keys()))
            )
        shutil.rmtree(join(self.themes_folder, __info__['name']), ignore_errors=True)
        # # Do not remove settings on uninstall.
        # # If you want to remove, uncomment the line below.
        # rmtree(_config_root_folder, ignore_errors=True)

        pip_check = shutil.which("pip")
        if pip_check is not None:
            subprocess.check_output(
                f'pip uninstall {__info__["name"]} -y',
                shell=True,
                universal_newlines=True,
            )
        utils.change_theme_in_zshrc(self.zsh_rc, "robbyrussell")

        if reply[0] == 1:
            shutil.rmtree(self.omz_root_folder, ignore_errors=True)
            with suppress(Exception):
                shutil.copyfile(
                    self.zsh_rc, f"{self.zsh_rc}-D{datetime.today().isoformat()}"
                )
            with suppress(Exception):
                os.remove(self.zsh_rc)

        utils.reload_zsh()

        printer("Uninstall process finished.", foreground=FG.FINISH)
