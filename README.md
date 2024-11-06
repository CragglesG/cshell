# CShell
CShell is an extensible, in-development, POSIX-compliant shell made with Python.

_Found a bug? Want a new feature? [Create an issue!](https://github.com/CragglesG/cshell/issues/new) (Please check for an existing one first to avoid duplicates.)_

_Want to contribute? You can find good first issues [here](https://github.com/CragglesG/cshell/contribute)._

## Table of Contents

- [Installation Guide](#installation-guide)
- [Features](#features)

## Installation Guide

CShell ony supports Linux at this time. Support for macOS and Windows may come soon.

To install CShell, execute this command:

```
git clone https://github.com/CragglesG/cshell cshell-install && cd cshell-install && ./install.sh
```

The above command clones the CShell repo, enters the cloned directory, and runs the install script. To update your user `PATH`, run:

```
source ~/.bashrc
```

You can now run CShell with the `cshell` command.

## Features

CShell is currently under heavy development, and is not yet complete. Here's a list of features that are available now:

- `exit`, `echo`, `type`, `pwd`, `cd`, `builtins`, `reload`, and `history` built-ins
- History and `.inputrc` support
- Extensions framework through `ShellExtension`
- Environment variables support
- Built-in `PATH` support
- Fallback to default system shell
