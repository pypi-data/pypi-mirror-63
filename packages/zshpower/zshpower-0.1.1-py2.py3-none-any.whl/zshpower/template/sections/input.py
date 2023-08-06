def template_input():
    data = {
        "input.zsh": """#!/usr/bin/env zsh
function snakypy_input () {
    local snakypy__input
    [[ $SSH_CONNECTION ]] && local SNAKYPY__INPUT_PROMPT_SYMBOL=">"
    snakypy__input="$(snakypy::fg "$SNAKYPY__INPUT_COLOR" "" \\
"$SNAKYPY__INPUT_PROMPT_SYMBOL" " ")"
    if [[ "$(id -u)" == "0" ]]; then
        snakypy__input="$(snakypy::fg red "" $SNAKYPY__INPUT_PROMPT_SYMBOL " ")"
    fi
    echo "${snakypy__input}"
}
SNAKYPY__APPLY_INPUT_PROMPT="$(snakypy_input)"
export SNAKYPY__APPLY_INPUT_PROMPT
"""
    }
    return data
