import snakypy
from zshpower import decorators
from zshpower.core import ZSHPower

core = ZSHPower()


@decorators.assign_cli(core.arguments, "init")
def init():
    core.init_command()


@decorators.assign_cli(core.arguments, "config")
def config_action():
    core.config_command()


@decorators.checking_init_command(core.themes_folder)
@decorators.assign_cli(core.arguments, "enable")
def enable():
    core.enable_command()


@decorators.assign_cli(core.arguments, "disable")
def disable():
    core.disable_command(core.arguments)


@decorators.assign_cli(core.arguments, "--credits")
def credence():
    core.credence_command()


@decorators.assign_cli(core.arguments, "reload")
def reload_config():
    core.reload_command()


@decorators.assign_cli(core.arguments, "reset")
def reset_config():
    core.reset_command()


@decorators.assign_cli(core.arguments, "uninstall")
def uninstall():
    core.uninstall_command()


@snakypy.decorators.use_unix_system
def main():
    (
        init(),
        enable(),
        disable(),
        credence(),
        uninstall(),
        config_action(),
        reset_config(),
        reload_config(),
    )
