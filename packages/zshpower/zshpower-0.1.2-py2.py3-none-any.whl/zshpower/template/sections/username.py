def template_username():
    data = {
        "username.zsh": """#!/usr/bin/env zsh
function snakypy_username () {
    local snakypy__username_data
    local snakypy__username
    local snakypy__username_suffix_root
    snakypy__username="$(snakypy::fg "$SNAKYPY__USERNAME_COLOR" "" "%n" " ")"
    if [[ $SNAKYPY__HOSTNAME_PREFIX_TEXT == "@" ]] &&
    [[ $SNAKYPY__HOSTNAME_ENABLE == True ]]; then
        snakypy__username="$(snakypy::fg "$SNAKYPY__USERNAME_COLOR" "" \\
"%n" "")"
    fi
    if [[ "$(id -u)" == "0" ]]; then
        snakypy__username_suffix_root="$(snakypy::fg green "" \\
"$SNAKYPY__USERNAME_SUFFIX_ROOT_TEXT" " ")"
        snakypy__username="$(snakypy::fg red "" "%n" " ")\\
${snakypy__username_suffix_root}"
        if [[ $SNAKYPY__HOSTNAME_PREFIX_TEXT == "@" ]] &&
        [[ $SNAKYPY__HOSTNAME_ENABLE == True ]]; then
            snakypy__username="$(snakypy::fg red "" "%n" "")\\
${snakypy__username_suffix_root}"
        fi
    fi
    if [[ $SNAKYPY__USERNAME_ENABLE == True ]] &&
    [[ $SNAKYPY__ENABLE_HOSTNAME_USERNAME_SSH == True ]] &&
    [[ "$(id -u)" != "0" ]] && [[ ! $SSH_CONNECTION ]] ||
    [[ $SNAKYPY__USERNAME_ENABLE == False ]]; then
        return
    else
        echo "${snakypy__username}"
    fi
}
SNAKYPY__APPLY_USERNAME="$(snakypy_username)"
export SNAKYPY__APPLY_USERNAME
"""
    }
    return data
