def template_git():
    data = {
        "git.zsh": """#!/usr/bin/env zsh
function snakypy_git_status () {
    snakypy::exists git || return
    local snakypy__git_prefix1
    local snakypy__git_prefix2
    local snakypy__git_symbol
    snakypy__git_prefix1="$(snakypy::fg red "" "$SNAKYPY__SEPARATOR" " ")"
    snakypy__git_prefix2="$(snakypy::fg "$SNAKYPY__GIT_PREFIX_COLOR" "" \\
"$SNAKYPY__GIT_PREFIX_TEXT" " ")"
    snakypy__git_symbol="$(snakypy::fg "$SNAKYPY__GIT_ICON_COLOR" "" \\
"$(snakypy::icon "\\uf418" "git:")" " ")"
    ZSH_THEME_GIT_PROMPT_PREFIX="${snakypy__git_prefix1}\\
${snakypy__git_prefix2}${snakypy__git_symbol}\\
$(snakypy::fg "$SNAKYPY__GIT_BRANCH_COLOR")"
    ZSH_THEME_GIT_PROMPT_SUFFIX=" "
    ZSH_THEME_GIT_PROMPT_CACHE="1"
    ZSH_THEME_GIT_PROMPT_DIRTY=""
    ZSH_THEME_GIT_PROMPT_CLEAN="$(snakypy::fg green " " \\
"$(snakypy::icon "\\uf62c" "!")" "")"
    ZSH_THEME_GIT_PROMPT_ADDED="$(snakypy::fg green "" \\
"$(snakypy::icon "\\uf44d" "+")" " ")"
    ZSH_THEME_GIT_PROMPT_MODIFIED="$(snakypy::fg blue "" \\
"$(snakypy::icon "\\uf8ea" "*")" " ")"
    ZSH_THEME_GIT_PROMPT_DELETED="$(snakypy::fg red "" \\
"$(snakypy::icon "\\uf655" "x")" " ")"
    ZSH_THEME_GIT_PROMPT_RENAMED="$(snakypy::fg magenta "" \\
"$(snakypy::icon "\\uf101" ">>")" " ")"
    ZSH_THEME_GIT_PROMPT_UNMERGED="$(snakypy::fg white "" \\
"$(snakypy::icon "\\uf6fb" "=")" " ")"
    ZSH_THEME_GIT_PROMPT_UNTRACKED="$(snakypy::fg yellow "" \\
"$(snakypy::icon "\\uf41e" "?")" " ")"
    ZSH_THEME_GIT_PROMPT_AHEAD="$(snakypy::fg blue " " \\
"$(snakypy::icon "\\uf55c" "^")" "")"
    ZSH_THEME_GIT_PROMPT_BEHIND="$(snakypy::fg yellow " " \\
"$(snakypy::icon "\\uf544" "_")" "")"
    ZSH_THEME_GIT_PROMPT_DIVERGED="$(snakypy::fg magenta " " \\
"$(snakypy::icon "\\ufb15" "<->")" "")"
    ZSH_THEME_GIT_PROMPT_CONFLICTS="$(snakypy::fg red " " \\
"$(snakypy::icon "\\uf0e7" "!=")" "")"
    ZSH_THEME_GIT_PROMPT_CHANGED="$(snakypy::fg blue " " \\
"$(snakypy::icon "\\uf8ea" "*")" "")"
    snakypy::is_enable "$SNAKYPY__GIT_ENABLE" "$(git_prompt_info)\\
$(git_prompt_status)"
}
SNAKYPY__APPLY_GIT_STATUS="\\$(snakypy_git_status)"
export SNAKYPY__APPLY_GIT_STATUS
"""
    }
    return data
