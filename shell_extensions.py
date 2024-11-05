from typing import Any, List, Callable
from shell_builtins import ShellBuiltins
from shell import Shell

class ShellExtension:
    """Base class for all CShell Extensions."""

    def __init__(self, name: str, func: Callable) -> None:        
        self.name = name
        self.func = func
    
    def register(self, append_extensions: Shell.append_extensions) -> None:
        append_extensions((self.name, self))
    
    def __call__(self, msg: List[str], pathfiles: List[str], builtins: ShellBuiltins, *args: Any, **kwds: Any) -> Any:
        self.func(msg, pathfiles, builtins, *args, **kwds)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"ShellExtension(\"{self.name}\", {self.func})"

