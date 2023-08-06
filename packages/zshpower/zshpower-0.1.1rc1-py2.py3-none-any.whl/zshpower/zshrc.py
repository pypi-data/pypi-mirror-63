import re
import snakypy
from datetime import datetime
from os.path import exists
from shutil import copyfile
from zshpower import _omz_root_folder


content = f'''
# Generate by: ZSHPower
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="{_omz_root_folder}"

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

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
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
plugins=(git)

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
'''


def read(zsh_rc):
    if exists(zsh_rc):
        with open(zsh_rc) as r:
            content_ = r.read()
        m = re.search(r"ZSH_THEME=\".*", content_)
        if m is not None:
            zsh_theme = m.group(0)
            lst = zsh_theme.split('=')
            theme_name = [s.strip('"') for s in lst][1]
            return theme_name, content_, zsh_theme
    return False


def create(content_, zsh_rc):
    if exists(zsh_rc):
        if not read(zsh_rc):
            copyfile(zsh_rc, f'{zsh_rc}-D{datetime.today().isoformat()}')
            snakypy.file.create(content_, zsh_rc, force=True)
            return True
    elif not exists(zsh_rc):
        snakypy.file.create(content_, zsh_rc)
        return True
    return


def plugins_current(zsh_rc):
    content_ = read(zsh_rc)[1]
    m = re.search(r"^plugins=\(.*", content_, flags=re.M)
    if m is not None:
        get = m.group(0)
        lst = get.split('=')
        current = [i.strip('"').replace('(', '').replace(')', '') for i in lst][1]
        return current.split()


def add_plugins(zsh_rc):
    plugins = ['zsh-syntax-highlighting', 'zsh-autosuggestions']
    current = plugins_current(zsh_rc)
    new_plugins = []
    for plugin in plugins:
        if plugin not in current:
            new_plugins.append(plugin)

    if len(new_plugins) > 0:
        plugins = f'plugins=({" ".join(current)} {" ".join(new_plugins)})'
        new_zsh_rc = re.sub(rf"^plugins=\(.*", plugins, read(zsh_rc)[1], flags=re.M)
        snakypy.file.create(new_zsh_rc, zsh_rc, force=True)
        return new_zsh_rc
    return


def change_theme(zsh_rc, theme_name):
    if read(zsh_rc):
        current_theme = read(zsh_rc)[2]
        new_theme = f'ZSH_THEME="{theme_name}"'
        new_zsh_rc = re.sub(rf'{current_theme}', new_theme, read(zsh_rc)[1], flags=re.M)
        snakypy.file.create(new_zsh_rc, zsh_rc, force=True)
        return True
    return
