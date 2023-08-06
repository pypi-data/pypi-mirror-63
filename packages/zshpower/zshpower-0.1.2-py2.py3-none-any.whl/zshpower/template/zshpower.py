from zshpower import __name__


def template_zshpower():
    data = {
        "zshpower.zsh-theme": f"""#!/usr/bin/env bash
SNAKYPY_ROOT="$ZSH_CUSTOM/themes/{__name__}"
export PATH="$SNAKYPY_ROOT:$PATH"
source "$SNAKYPY_ROOT"/variables.zsh
source "$SNAKYPY_ROOT"/preferences.zsh
    function _load_libs() {{
        for lib in "$SNAKYPY_ROOT"/lib/*.zsh; do
            source "$lib"
        done
    }}
    _load_libs
    function _load_sections() {{
        for section in "$SNAKYPY_ROOT"/sections/*.zsh; do
            source "$section"
        done
    }}
    _load_sections
prompt
"""
    }
    return data
