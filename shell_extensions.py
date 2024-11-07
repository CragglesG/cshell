from typing import Any, List, Callable
from shell_builtins import ShellBuiltins

class ShellExtension:
    """Base class for all CShell Extensions."""

    def __init__(self, name: str, func: Callable) -> None:        
        self.name = name
        self.func = func

    def __call__(self, msg: List[str], pathfiles: List[str], builtins: ShellBuiltins, send: Callable, *args: Any, **kwds: Any) -> List[str]:
        self.func(msg, pathfiles, builtins, send, *args, **kwds)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"ShellExtension(\"{self.name}\", {self.func})"
    
    def register(self, append_extensions: Callable) -> None:
        append_extensions((self.name, self))
    

