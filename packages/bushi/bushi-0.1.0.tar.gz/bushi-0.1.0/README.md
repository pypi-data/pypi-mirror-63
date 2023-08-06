# Bushi

This package contains functions to handle commands in a **Linux** based terminal.
The main purpose of this package is to replace **Shell Script** with a simplier **Python** based functions.

# Target

## Version 1.0

### Major

- ~~Terminal input and output formatting.~~ _(done since `0.1.0`)_
- Manage multiple sessions with `tmux` command.
- Build a **ROS** based package with `colcon` command.
- Manage a **Git** repository with `git` command.
- Manage an **APT** package with `apt-get` command.

# Changelogs

## Version 0.1.0

- Add `io` class that handle terminal input and output with the following functionality:
  - Output to the terminal using `info()`, `warn()`, `fail()`, `succes()`, `info_list()`, `warn_list()`, `fail_list()`, `success_list()`, and `process()`.
  - Input from the terminal using `ask()`, and `ask_secret()`.
  - Both input and output will emphasize a string between `*`. _(ex: `*here*`)_
  - Exit current process using `terminate()`.
    With empty argument, this function will return `0`.
    Else, it will output the arguments and return `1`.