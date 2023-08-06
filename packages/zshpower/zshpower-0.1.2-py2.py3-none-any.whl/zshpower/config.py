from datetime import datetime
from zshpower import __version__, __name__


def config_content():
    date_format = datetime.today().isoformat()
    data = f"""# Generate by: ZSHPower - D{date_format}
# Version: {__version__}
# ---------------------------------------------------------------------
# NOTE: If you edit this file outside of "{__name__} config --open",
# run the "{__name__} reload" command for the changes to take effect.
# For more information, see the documentation at:
# https://github.com/snakypy/zshpower#configuration-file

[general]
separator = ""
negative.enable = false

[username]
enable = true
color = "cyan"
root.suffix = "in"

[hostname]
enable = true
color = "magenta"
prefix.color = "green"
prefix.text = "at"

[path]
color = "cyan"
involved = ""
prefix.color = "green"
prefix.text = "in"
abspath.enable = false

[git]
enable = true
branch.color = "cyan"
prefix.color = "green"
prefix.text = "on"
symbol.color = "white"

[input]
symbol = "\\uf553"
color = "green"

[pyproject]
enable = true
color = "magenta"
prefix.color = "green"
prefix.text = "on"

[python]
color = "yellow"
prefix.color = "green"
prefix.text = "via"
version.enable = true
version.minor.enable = true
version.micro.enable = true

[ssh]
enable = true
color = "magenta"
prefix.color = "green"
prefix.text = "via"
userhost.enable = true

[virtualenv]
enable = true
color = "yellow"
prefix.color = "green"
prefix.text = "via"

[virtualenv.name]
normal.enable = true
text = "venv"
    """
    return data


def zshrc_content(omz_root):
    data = f"""# Generate by: ZSHPower
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="{omz_root}"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="zshpower"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for
# completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large
# repositories much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution
# time stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git python django pip pep8 autopep8)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
    """
    return data
