from snakypy.console import cmd
from snakypy import printer, FG
from os.path import exists, join


def install(omz_root_folder):
    cmd_line = f'git clone https://github.com/ohmyzsh/ohmyzsh.git {omz_root_folder}'
    try:
        if not exists(omz_root_folder):
            printer('Install Oh My ZSH...', foreground=FG.QUESTION)
            cmd(cmd_line, verbose=True)
            printer('Oh My ZSH installation process finished.', foreground=FG.FINISH)
    except Exception:
        raise Exception('Error downloading Oh My ZSH. Aborted!')


def install_plugins(omz_root_folder, plugins: list):
    try:
        for plugin in plugins:
            path = join(omz_root_folder, f"custom/plugins/{plugin}")
            clone = f"git clone https://github.com/zsh-users/{plugin}.git {path}"
            if not exists(path):
                printer(f'Install plugins {plugin}...', foreground=FG.QUESTION)
                cmd(clone, verbose=True)
                printer(f'Plugin {plugin} task finished!', foreground=FG.FINISH)
    except Exception:
        raise Exception(f'There was an error installing the plugin')
