def template_virtualenv():
    data = {
        "virtualenv.zsh": """#!/usr/bin/env zsh
export VIRTUAL_ENV_DISABLE_PROMPT=yes
function snakypy_virtualenv () {
    snakypy::exists python || return
    local snakypy__virtualenv_prefix1
    local snakypy__virtualenv_prefix2
    local snakypy__virtualenv
    snakypy__virtualenv_prefix1="$(snakypy::fg red "" "$SNAKYPY__SEPARATOR" " ")"
    snakypy__virtualenv_prefix2="$(snakypy::fg "$SNAKYPY__VIRTUALENV_PREFIX_COLOR" "" \\
"$SNAKYPY__VIRTUALENV_PREFIX_TEXT" " ")"
    if [[ $VIRTUAL_ENV ]] && \\
[[ $SNAKYPY__VIRTUALENV_NAME_NORMAL_ENABLE == True ]]; then
        snakypy__virtualenv="$(snakypy::fg "$SNAKYPY__VIRTUALENV_COLOR" "" \\
\\("$(basename "$VIRTUAL_ENV")"\\) " ")"
    elif [[ $VIRTUAL_ENV ]] && \\
[[ $SNAKYPY__VIRTUALENV_NAME_NORMAL_ENABLE == False ]]; then
        snakypy__virtualenv="$(snakypy::fg "$SNAKYPY__VIRTUALENV_COLOR" "" \\
\\("$SNAKYPY__VIRTUALENV_TEXT"\\) " ")"
    fi
    if [[ $VIRTUAL_ENV ]] &&
    [[ $SNAKYPY__VIRTUALENV_ENABLE == True ]]; then
        echo "${snakypy__virtualenv_prefix1}${snakypy__virtualenv_prefix2}\\
${snakypy__virtualenv}"
    fi
}
SNAKYPY__APPLY_VIRTUALENV="\\$(snakypy_virtualenv)"
export SNAKYPY__APPLY_VIRTUALENV
"""
    }
    return data
