import os
import pwd
import subprocess
from snakypy import printer, FG


def reload_zsh():
    subprocess.call('exec zsh', shell=True)


def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])


def current_shell():
    pw = pwd.getpwuid(os.getuid())
    path_shell = pw[-1]
    shell = str(path_shell).split('/')[-1]
    return shell, path_shell


def current_user():
    return str(os.popen("whoami").read()).replace('\n', '')


def change_shell():
    if current_shell()[0] != 'zsh':
        try:
            subprocess.call(f"chsh -s $(which zsh) {current_user()}", shell=True)
        except KeyboardInterrupt:
            printer('Canceled by user', foreground=FG.WARNING)
