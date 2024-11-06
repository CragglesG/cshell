import sys
import os
import Levenshtein
import readline
import importlib

from shell_builtins import ShellBuiltins
from shell_extensions import ShellExtension
from typing import Tuple, Callable
from colours import RED, DEFAULT

class Shell:
    def __init__(self):
        # Initialize the readline module
        readline.set_auto_history(True)
        readline.read_history_file(os.path.expanduser("~/.cshell/.history"))
        readline.set_history_length(100)
        readline.read_init_file(os.path.expanduser("~/.cshell/.inputrc"))

        # Set up the utility variables
        self.path_files = {}
        self.extensions = {}
        self.load_extensions()
        self.builtins = ShellBuiltins(readline, self.path_files, self.extensions)
        self.path = os.environ.get("PATH").split(":")
        
        # Fill up self.path_files with {name:path} entries
        for entry in self.path:
            if os.path.exists(entry):
                for content in os.scandir(entry):
                    if os.path.isfile(content.path):
                        self.path_files[content.name] = content.path
    
    def __call__(self):
            """Call the main method."""
            self.main()
        
    def __str__(self):
        return "CShell Instance"
    
    def __repr__(self):
        return "Shell()"
    
    def load_extensions(self):
        # Load all extensions from the extensions directory
        extensions_dir = "extensions"
        if not os.path.isdir(extensions_dir):
            return
        for filename in os.listdir(extensions_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                module = importlib.import_module(f"extensions.{module_name}")
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, ShellExtension) and cls != ShellExtension:
                        extension = cls()
                        extension.register(self.append_extensions)
    
    def append_extensions(self, new_builtin: Tuple[str, Callable]) -> None:
        # Append the new extension to the extensions dictionary
        self.extensions[new_builtin[0]] = new_builtin[1]
                    
    def ask(self) -> None:
        # Return a list of the command and arguments
        try:
            msg = input("$ ")
        except KeyboardInterrupt:
            self.send("\nWoah! Are you trying to kill me!? Next time, just type exit if you want me to go away.\n")
            self.exit()
        return msg.split(" ")

    def send(self, msg: str) -> None:
        # Print to the command line
        sys.stdout.write(msg)
        sys.stdout.flush()

    def exit(self, msg: list[str] = ["exit"]) -> None:
        readline.append_history_file(readline.get_current_history_length(), os.path.expanduser("~/.cshell/.history"))

        if len(msg) == 1:
            os._exit(0)
        else:
            os._exit(int(msg[1]))

    def main(self):
        # Ask for input and read it
        msg = self.ask()

        # Respond to the input appropriately
        match msg[0]:
            # Exit from the shell
            case "exit":
                self.exit(msg)

            # # Echo the arguments
            # case "echo":
            #     if " ".join(msg[1:]).count("$") == 0:
            #         self.send(" ".join(msg[1:]) + "\n")
            #     else:
            #         for i in msg[1:]:
            #             if i[0] == "$":
            #                 self.send(os.environ.get(i[1:]) + " ")
            #             else:
            #                 self.send(i + " ")
            #         self.send("\n")

            # # Check whether the first argument is a builtin, an executable, or not found
            # case "type":
            #     if len(msg) != 1:
            #         if msg[1] in self.builtins:
            #             self.send(msg[1] + " is a shell builtin\n")
            #         elif msg[1] in self.path_files.keys():
            #             self.send(f"{msg[1]} is {self.path_files[msg[1]]}\n")
            #         else:
            #             self.send(f"type: {msg[1]}: not found\n")

            # # Print the working directory
            # case "pwd":
            #     self.send(os.getcwd() + "\n")

            # # Change the working directory
            # case "cd":
            #     if len(msg) == 1:
            #         os.chdir(os.environ.get("HOME"))

            #     if os.path.isdir(msg[1]):
            #         os.chdir(msg[1])
            #     elif msg[1] == "~":
            #         os.chdir(os.environ.get("HOME"))
            #     elif os.path.isfile(msg[1]):
            #         self.send(f"cd: {msg[1]}: Not a directory")
            #     else:
            #         self.send(f"cd: {msg[1]}: No such file or directory\n")
            
            # case "builtins":
            #     self.send(" ".join(self.builtins) + "\n")

            # case "reload":
            #     if len(msg) > 1:
            #         if msg[1] == "--install" or msg[1] == "-i":
            #             os.system("~/.cshell/install.sh")
            #     os.system("reset")
            #     os._exit(121)
                
            # case "history":
            #     self.send("\n".join(self.history) + "\n")    
            
            # Execute builtins
            case builtin if builtin in self.builtins.keys():
                to_send = self.builtins[builtin](msg)
                if type(to_send) == list:
                    for string in to_send:
                        self.send(string)
            
            # Execute extensions
            case extension if extension in self.extensions.keys():
                to_send = self.extensions[extension](msg, self.path_files, self.builtins)
                if type(to_send) == list:
                    for string in to_send:
                        self.send(string)

            # Execute executables in path
            case cmd if cmd in self.path_files.keys():
                os.system(f"{self.path_files[cmd]} {" ".join(msg[1:])}")

            # Handle empty input
            case "":
                self.send("\n")
            
            # Catch all other cases
            case _:
                self.send(f"{RED}{msg[0]}: command not found{DEFAULT}\n")
                distances = {'null':0}
                for cmd in [*self.builtins, *self.path_files, *self.extensions]:
                    distances[cmd] = Levenshtein.jaro(msg[0], cmd, score_cutoff=0.8)
                if max(distances, key=distances.get) != 'null':
                    self.send(f"Did you mean {max(distances, key=distances.get)}?\n")
        try:        
            self.main()
        except Exception as err:
            self.send(f"Oops! It looks like an error occured! Here's some more details: {err}\n")
        finally:
            self.main()
