def template_pyproject():
    data = {
        "pyproject.zsh": """#!/usr/bin/env zsh
function snakypy_pyproject () {
    local snakypy__pyproject_prefix1
    local snakypy__pyproject_prefix2
    local get_version
    local snakypy__pyproject
    snakypy__pyproject_prefix1="$(snakypy::fg red "" \\
"$SNAKYPY__SEPARATOR" " ")"
    snakypy__pyproject_prefix2="$(snakypy::fg \\
"$SNAKYPY__PYPROJECT_PREFIX_COLOR" "" "$SNAKYPY__PYPROJECT_PREFIX_TEXT" " ")"
    [[ -f "$(pwd)/pyproject.toml" ]] && \\
    get_version=$(< pyproject.toml sed -n '/^version/p' | \\
cut -d'"' -f2 | cut -d"'" -f2)
    [[ -z $get_version ]] && get_version="None"
    snakypy__pyproject="$(snakypy::fg "$SNAKYPY__PYPROJECT_COLOR" "" \\
"$(snakypy::icon "\\uf8d6 " "pkg-")${get_version}" " ")"
    if [[ -f "$(pwd)/pyproject.toml" ]] &&
    [[ $SNAKYPY__PYPROJECT_ENABLE == True ]]; then
        echo "${snakypy__pyproject_prefix1}${snakypy__pyproject_prefix2}\\
${snakypy__pyproject}"
    fi
}
SNAKYPY__APPLY_PYPROJECT="\\$(snakypy_pyproject)"
export SNAKYPY__APPLY_PYPROJECT
"""
    }
    return data
