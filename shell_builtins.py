import readline
import os
from typing import List, Callable
from colours import RED, DEFAULT, BLUE

class ShellBuiltins:
    """Built-in CShell commands."""

    def __init__(self, readline_instance: readline, path_files: dict, extensions: dict, send: Callable) -> None:
        self.readline = readline_instance
        self.builtins = {"exit": None, "echo": self.echo, "type": self.type, "pwd": self.pwd, "cd": self.cd, "builtins": self.builtins_func, "reload": self.reload, "history": self.history}
        self.path_files = path_files
        self.extensions = extensions
        self.send = send

    def __getitem__(self, key: str) -> List[str]:
        return self.builtins[key]
    
    def keys(self) -> List[str]:
        return list(self.builtins.keys())
    
    def __iter__(self) -> List[str]:
        return iter(self.builtins)
    
    def __len__(self) -> int:
        return len(self.builtins)
    
    def __str__(self) -> str:
        return ", ".join(self.builtins.keys())
    
    def __repr__(self) -> str:
        return f"ShellBuiltins([{'\", \"'.join(self.builtins) + '\"'}])"
    
    def error(self, msg: str) -> None:
        self.send(f"{RED}{msg}{DEFAULT}")
    
    # def exit(self, msg: list[str] = ["exit"]) -> None:
    #     self.readline.append_history_file(self.readline.get_current_history_length(), os.path.expanduser("~/.cshell/.history"))

    #     if len(msg) == 1:
    #         os._exit(0)
    #     else:
    #         os._exit(int(msg[1]))
    
    def echo(self, msg: list[str]) -> List[str]:
        if " ".join(msg[1:]).count("$") == 0:
            self.send(" ".join(msg[1:]) + "\n")
        else:
            for i in msg[1:]:
                if i[0] == "$":
                    self.send(os.environ.get(i[1:]) + " ")
                else:
                    self.send(i + " ")
            self.send("\n")
        

    def type(self, msg: List[str]) -> List[str]:
        if len(msg) != 1:
            if msg[1] in self.builtins:
                self.send(msg[1] + " is a shell builtin\n")
            elif msg[1] in self.path_files.keys():
                self.send(f"{msg[1]} is {self.path_files[msg[1]]}\n")
            elif msg[1] in self.extensions.keys():
                self.send(f"{msg[1]} is a shell extension\n")
            else:
                self.error(f"type: {msg[1]}: not found")
                self.send("\n")
        else:
            self.error("type: not enough arguments")
            self.send("\n")
    
    def pwd(self, msg: List[str]) -> List[str]:
        self.send(os.getcwd() + "\n")

    def cd(self, msg: List[str]) -> List[str]:

        if len(msg) == 1:
            os.chdir(os.environ.get("HOME"))

        if os.path.isdir(msg[1]):
            os.chdir(msg[1])
        elif msg[1] == "~":
            os.chdir(os.environ.get("HOME"))
        elif msg[1].count("~") != 0:
            os.chdir(os.path.expanduser(msg[1]))
        elif os.path.isfile(msg[1]):
            self.error(f"cd: {msg[1]}: Not a directory")
            self.send("\n")
        else:
            self.error(f"cd: {msg[1]}: No such file or directory")
            self.send("\n")
        
    
    def builtins_func(self, msg: List[str]) -> List[str]:
        self.send(" ".join(self.builtins.keys()) + "\n")

    def reload(self, msg: List[str]) -> List[str]:
        if len(msg) > 1:
            if msg[1] == "--install" or msg[1] == "-i":
                os.system("~/.cshell/install.sh")
        os.system("reset")
        os._exit(121)
    
    def history(self, msg: List[str]) -> List[str]:
        self.readline.append_history_file(self.readline.get_current_history_length(), os.path.expanduser("~/.cshell/.history"))
        self.readline.read_history_file(os.path.expanduser("~/.cshell/.history"))
        with open(os.path.expanduser("~/.cshell/.history"), "r") as f:
            history = f.readlines()
        self.send("".join(history))
    