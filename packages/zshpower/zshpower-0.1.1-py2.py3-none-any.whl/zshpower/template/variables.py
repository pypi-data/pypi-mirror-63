def template_variables():
    data = {
        "variables.zsh": """#!/usr/bin/env zsh
SNAKYPY__PYTHON_EXEC="python"
SNAKYPY__SPACE=" "
SNAKYPY__JUMPLINE="
"
export SNAKYPY__PYTHON_EXEC SNAKYPY__ARROW SNAKYPY__SPACE SNAKYPY__JUMPLINE
"""
    }
    return data
