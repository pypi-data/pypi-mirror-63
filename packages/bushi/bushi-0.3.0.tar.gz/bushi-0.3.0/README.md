# Bushi

This package contains functions to handle commands in a **Linux** based terminal.
The main purpose of this package is to replace **Shell Script** with a simplier **Python** based functions.

# Target

## Version 1.0

### Major

- ~~Terminal input and output formatting.~~ _(done since `0.1.0`)_
- ~~Manage multiple sessions with `tmux` command~~. _(done since `0.3.0`)_
- Build a **ROS** based package with `colcon` command.
- Manage a **Git** repository with `git` command.
- Manage an **APT** package with `apt-get` command.

### Minor

- ~~`cmd.run()` must preserve the output formating.~~ _(aborted, `cmd.run()` changes to not pipe output)_

# Changelogs

## Version 0.3.0 _(14/03/2020)_

- Add `tmux` class that handle multiple session with the following functionalities:
  - Check existence of a session using `tmux.session_exist()`.
  - Kill a session using `tmux.session_kill()`.
  - Detach from current session using `tmux.detach()`.
  - Run a separate process with output on different session using `tmux.session_run()` with the following functionalities:
    - It will call `bushi-tmux-runner` that handle how the process is called and how it return the process returncode to the parent process.
    - It uses to replace `tmux.run()` where we want to do a process while viewing its output.
    - Process failed when the **tmux** session was detached.
    - On keyboard interrupt, or when the process failed, it will continue with detaching the current session.
- Modify functions in `io` as follow:
  - Change how a process thread is called, it will only be created when needed, else it will be destroyed.
  - Call `io.process_stop()` instead of changing `io.__process_text` to stop the process thread.
  - Add `io.press_enter()` function that try to wait for `enter` key before continue the program.
  - Add `io.ask_yes_no()` function that will ask question that accept `yes` or `no` input and return that value as `True` and `False` respectively.
    If the input is invalid, it will terminate the program.
- Modify a function in `cmd` as follow:
  - Change `cmd.run()` to call `subprocess.run()` instead of `subprocess.pOpen()` that pipe the output to the parent process.

## Version 0.2.0 _(13/03/2020)_

- Add `cmd` class that handle subprocess run with the following functionalities:
  - `run()` to run a subprocess with outputs.
  - `runmuted()` to run a subprocess without any outputs.
- Add `path` class that handle files and directories with the following functionalities:
  - Check existence of files and directories using `isfile()`, and `isdir()`.
  - Get and change working directory using `getdir()` and `changedir()` respectively.
  - Some others functionality that also exist in the `os.path`.
- Modify functions in the `io` as follow:
  - Change how output should behave.
  - Modify output format for the process command.
  - Change how process symbol be animated.
  - Output the duration in the process command.

## Version 0.1.0 _(12/03/2020)_

- Add `io` class that handle terminal input and output with the following functionalities:
  - Output to the terminal using `info()`, `warn()`, `fail()`, `succes()`, `info_list()`, `warn_list()`, `fail_list()`, `success_list()`, and `process()`.
  - Input from the terminal using `ask()`, and `ask_secret()`.
  - Both input and output will emphasize a string between `*`. _(ex: `*here*`)_
  - Exit current process using `terminate()`.
    With empty argument, this function will return `0`.
    Else, it will output the arguments and return `1`.