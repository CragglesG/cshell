# CShell
CShell is an extensible, in-development, POSIX-compliant shell made with Python.

_Found a bug? Want a new feature? [Create an issue!](https://github.com/CragglesG/cshell/issues/new) (Please check for an existing one first to avoid duplicates.)_

_Want to contribute? You can find good first issues [here](https://github.com/CragglesG/cshell/contribute)._

## Table of Contents

- [Installation Guide](#installation-guide)
- [Features](#features)
- [`ShellExtension` and the CShell Extension Framework](#shellextension-and-the-cshell-extension-framework)

## Installation Guide

CShell ony supports Linux at this time. Support for macOS and Windows may come soon.

To install CShell, execute this command:

```sh
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

## `ShellExtension` and the CShell Extension Framework

The CShell Extension Framework allows developers to extend CShell using the `ShellExtension` class. Extensions are provided with the user input, path files, and built-ins available in the current session, along with a function to display output to the user. Below is an example of a simple CShell extension:

```python
from shell_extensions import ShellExtension

class TestExtension(ShellExtension):
    def __init__(self):
        super().__init__("test-extension", self.test)
    
    def test(self, msg, pathfiles, builtins, send):
        send("This is a test extension\n")
```

The above extension displays the output `This is a test extension` to the user, followed by a newline. The newline is necessary to move the prompt to the next line. The `super().__init__` function takes two arguments, the extension command and the function to call.

All extensions should be located in `~/.cshell/extensions/`. CShell will scan this folder for extensions and register them upon starting.

> **Important:**
> CShell first searches for commands in the built-ins dictionary, followed by the extensions dictionary, and finally the path files dictionary. Extensions can therefore override path files, but not built-ins.