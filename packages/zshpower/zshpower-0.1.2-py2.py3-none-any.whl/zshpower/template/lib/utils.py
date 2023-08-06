def template_utils():
    data = {
        "utils.zsh": """#!/usr/bin/env zsh
function snakypy::exists () {
  command -v $1 > /dev/null 2>&1
}
function snakypy_fg_core () {
    use_prefix="%{${fg[$1]}%}${2}${3}${4}"
    just_color="%{${fg[$1]}%}"
}
function snakypy::fg () {
    local use_prefix
    local just_color
    local color=$1
    local spacing_initial=$2
    local element=$3
    local spacing_final=$4
    snakypy_fg_core "$color" "$spacing_initial" "$element" "$spacing_final"
    [[ $SNAKYPY__NEGATIVE_COLOR_ENABLE == True ]] && snakypy_fg_core "white" \\
"$spacing_initial" "$element" "$spacing_final"
    [[ $element ]] && echo -e "$use_prefix" || echo "$just_color"
}
function snakypy::is_enable () {
    if [[ $1 == True ]]; then
        echo "$2"
    fi
}
function snakypy::icon () {
    icon="$1"
    [[ $SSH_CONNECTION ]] && icon="$2"
    echo "$icon"
}
"""
    }
    return data
