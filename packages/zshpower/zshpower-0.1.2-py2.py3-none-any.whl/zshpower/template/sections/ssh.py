def template_ssh():
    data = {
        "ssh.zsh": """#!/usr/bin/env zsh
function snakypy_ssh () {
    snakypy::exists ssh || return
    local snakypy__ssh_prefix1
    local snakypy__ssh_prefix2
    local ssh_get
    snakypy__ssh_prefix1="$(snakypy::fg red " " "$SNAKYPY__SEPARATOR" "")"
    snakypy__ssh_prefix2="$(snakypy::fg "$SNAKYPY__SSH_PREFIX_COLOR" "" \\
"$SNAKYPY__SSH_PREFIX_TEXT" " ")"

    ssh_get="$(snakypy::fg "$SNAKYPY__SSH_COLOR" "" "$(snakypy::icon \\
"\\uf817")SSH" " ")"

    if [[ $SSH_CONNECTION ]] &&
    [[ $SNAKYPY__SSH_ENABLE == True ]]; then
        echo "${snakypy__ssh_prefix1}${snakypy__ssh_prefix2}${ssh_get}"
    fi
}
SNAKYPY__APPLY_SSH="$(snakypy_ssh)"
export SNAKYPY__APPLY_SSH
"""
    }
    return data
