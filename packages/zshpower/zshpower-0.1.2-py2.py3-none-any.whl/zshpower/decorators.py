from functools import wraps
from sys import exit
from os.path import exists, join
from snakypy import printer, FG
from zshpower import __info__, __name__


def assign_cli(arguments: callable(object), command: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if arguments(*args)[command]:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def checking_init_command(root: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not exists(join(root, f"{__name__}.zsh-theme")):
                printer(
                    f'Command "{__info__["name"]} init" has not been started.'
                    "Aborted",
                    foreground=FG.WARNING,
                )
                exit(1)
            return func(*args, **kwargs)

        return wrapper

    return decorator
