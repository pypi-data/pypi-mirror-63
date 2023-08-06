def template_path():
    data = {
        "path.zsh": """#!/usr/bin/env zsh
function snakypy_path_dir () {
    local snakypy__prefix_path_dir
    local count_involved
    local involved_element_0
    local involved_element_1
    local snakypy__path_dir_data
    local snakypy__path_dir_formated
    local snakypy__path_dir
    if  [[ $SNAKYPY__USERNAME_ENABLE == True ]] ||
        [[ $SNAKYPY__HOSTNAME_ENABLE == True ]]; then
        if [[ $SNAKYPY__ENABLE_HOSTNAME_USERNAME_SSH == False ]]; then
            snakypy__prefix_path_dir="$(snakypy::fg \\
"$SNAKYPY__PATH_DIR_PREFIX_COLOR" "" "$SNAKYPY__PATH_DIR_PREFIX_TEXT" " ")"
        elif [[ $SNAKYPY__ENABLE_HOSTNAME_USERNAME_SSH == True ]] &&
        [[ $SSH_CONNECTION ]]; then
            snakypy__prefix_path_dir="$(snakypy::fg \\
"$SNAKYPY__PATH_DIR_PREFIX_COLOR" "" "$SNAKYPY__PATH_DIR_PREFIX_TEXT" " ")"
        fi
    fi
    count_involved=$($SNAKYPY__PYTHON_EXEC -c \\
"print(len('$SNAKYPY__PATH_FOLDER_INVOLVED'))")
    if [[ ! $SNAKYPY__PATH_FOLDER_INVOLVED == "" ]] &&
    [[ $count_involved == "2" ]]; then
        involved_element_0="$($SNAKYPY__PYTHON_EXEC -c \\
"print('$SNAKYPY__PATH_FOLDER_INVOLVED'[0])")"
        involved_element_1="$($SNAKYPY__PYTHON_EXEC -c \\
"print('$SNAKYPY__PATH_FOLDER_INVOLVED'[1])")"
    fi
    if [[ $SNAKYPY__ABSOLUTE_PATH_ENABLE == True ]]; then
        snakypy__path_dir_data="${involved_element_0}\\
$(snakypy::icon "\\ufc6e ")%d${involved_element_1}"
    else
        snakypy__path_dir_data="${involved_element_0}\\
$(snakypy::icon "\\ufc6e ")%c${involved_element_1}"
    fi
    snakypy__path_dir_formated="$(snakypy::fg \\
"$SNAKYPY__PATH_FOLDER_COLOR" "" "$snakypy__path_dir_data" " ")"
    snakypy__path_dir="${snakypy__prefix_path_dir}\\
${snakypy__path_dir_formated}"
    echo "${snakypy__path_dir}"
}
SNAKYPY__APPLY_PATH_DIR="$(snakypy_path_dir)"
export SNAKYPY__APPLY_PATH_DIR
"""
    }
    return data
