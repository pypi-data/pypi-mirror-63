def template_hostname():
    data = {
        "hostname.zsh": """#!/usr/bin/env zsh
function snakypy_hostname () {
    local snakypy__hostname_prefix
    local snakypy__hostname
    snakypy__hostname_prefix="$(snakypy::fg "$SNAKYPY__HOSTNAME_PREFIX_COLOR" "" \\
"$SNAKYPY__HOSTNAME_PREFIX_TEXT" " ")"
    if [[ $SNAKYPY__HOSTNAME_PREFIX_TEXT == "@" ]]; then
        snakypy__hostname_prefix="$(snakypy::fg "$SNAKYPY__HOSTNAME_PREFIX_COLOR" "" \\
"$SNAKYPY__HOSTNAME_PREFIX_TEXT" "")"
    fi
    [[ $SNAKYPY__USERNAME_ENABLE == False ]] && snakypy__hostname_prefix=""
    snakypy__hostname="$(snakypy::fg "$SNAKYPY__HOSTNAME_COLOR" "" "%m" " ")"
    if  [[ $SNAKYPY__HOSTNAME_ENABLE == True ]] &&
        [[ $SNAKYPY__ENABLE_HOSTNAME_USERNAME_SSH == True ]] &&
        [[ ! $SSH_CONNECTION ]] ||
        [[ $SNAKYPY__HOSTNAME_ENABLE == False ]]; then
        return
    else
        echo "${snakypy__hostname_prefix}${snakypy__hostname}"
    fi
}
SNAKYPY__APPLY_HOSTNAME="$(snakypy_hostname)"
export SNAKYPY__APPLY_HOSTNAME
"""
    }
    return data
