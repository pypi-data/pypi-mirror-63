def template_python():
    data = {
        "python.zsh": """#!/usr/bin/env zsh
function snakypy_py_version () {
    snakypy::exists python || return
    local snakypy__python_version_prefix1
    local snakypy__python_version_prefix2
    local snakypy__python_version_minor
    local snakypy__python_version_micro
    local get_version
    local snakypy__python_version
    local search_files
    snakypy__python_version_prefix1="$(snakypy::fg red "" \\
"$SNAKYPY__SEPARATOR" " ")"
    snakypy__python_version_prefix2="$(snakypy::fg \\
"$SNAKYPY__PYTHON_PREFIX_COLOR" "" "$SNAKYPY__PY_VERSION_PREFIX_TEXT" " ")"
    [[ $SNAKYPY__PY_VERSION_MINOR_ENABLE == True ]] && \\
snakypy__python_version_minor=".{0[1]}"
    [[ $SNAKYPY__PY_VERSION_MICRO_ENABLE == True ]] && \\
snakypy__python_version_micro=".{0[2]}"
    get_version="$($SNAKYPY__PYTHON_EXEC -c "import sys; print('{0[0]}\\
${snakypy__python_version_minor}${snakypy__python_version_micro}'\\
.format(sys.version_info))")"
    snakypy__python_version="$(snakypy::fg "$SNAKYPY__PYTHON_COLOR" "" \\
"$(snakypy::icon "\\uf81f " "py-")${get_version}" " ")"
    search_files=(__pycache__ manage.py setup.py __init__.py \\
.python-version requirements.txt pyproject.toml)
    if [[ $SNAKYPY__PY_VERSION_ENABLE == True ]]; then
        for i in "${search_files[@]}"; do
            [[ -f $i ]] || [[ -d $i ]] || [[ $VIRTUAL_ENV ]] && \\
            echo "${snakypy__python_version_prefix1}\\
${snakypy__python_version_prefix2}${snakypy__python_version}" && break
        done
    fi
}
SNAKYPY__APPLY_PY_VERSION="\\$(snakypy_py_version)"
export SNAKYPY__APPLY_PY_VERSION
"""
    }
    return data
