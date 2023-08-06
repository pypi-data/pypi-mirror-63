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

### Minor

- `cmd.run()` must preserve the output formating.

# Changelogs

## Version 0.2.0 _(13/03/2020)_

- Add `cmd` class that handle subprocess run with the following functionality:
  - `run()` to run a subprocess with outputs.
  - `runmuted()` to run a subprocess without any outputs.
- Add `path` class that handle files and directories with the following functionality:
  - Check existence of files and directories using `isfile()`, and `isdir()`.
  - Get and change working directory using `getdir()` and `changedir()` respectively.
  - Some others functionality that also exist in the `os.path`.
- Modify functions in the `io` as follow:
  - Change how output should behave.
  - Modify output format for the process command.
  - Change how process symbol be animated.
  - Output the duration in the process command.

## Version 0.1.0 _(12/03/2020)_

- Add `io` class that handle terminal input and output with the following functionality:
  - Output to the terminal using `info()`, `warn()`, `fail()`, `succes()`, `info_list()`, `warn_list()`, `fail_list()`, `success_list()`, and `process()`.
  - Input from the terminal using `ask()`, and `ask_secret()`.
  - Both input and output will emphasize a string between `*`. _(ex: `*here*`)_
  - Exit current process using `terminate()`.
    With empty argument, this function will return `0`.
    Else, it will output the arguments and return `1`.