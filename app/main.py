import sys
import os

class Shell:
    def __init__(self):
        self.builtins = ["exit", "echo", "type", "pwd", "cd"]
        self.path = os.environ.get("PATH").split(":")
        self.path_files = {}

        for entry in self.path:
            if os.path.exists(entry):
                for content in os.scandir(entry):
                    if os.path.isfile(content.path):
                        self.path_files[content.name] = content.path
                    
    def ask(self) -> None:
        # Signal for input
        self.send("$ ")

        msg = input()
        return msg.split(" ")

    def send(self, msg: str) -> None:
        sys.stdout.write(msg)
        sys.stdout.flush()

    def main(self):
        msg = self.ask()
        match msg[0]:
            case "exit":
                sys.exit(int(msg[1]))
            case "echo":
                self.send(" ".join(msg[1:]) + "\n")
            case "type":
                if msg[1] in self.builtins:
                    self.send(msg[1] + " is a shell builtin\n")
                elif msg[1] in self.path_files.keys():
                    self.send(f"{msg[1]} is {self.path_files[msg[1]]}\n")
                else:
                    self.send(msg[1] + ": not found\n")
            case "pwd":
                self.send(os.getcwd() + "\n")
            case "cd":
                if os.path.exists(msg[1]):
                    os.chdir(msg[1])
                elif msg[1] == "~":
                    os.chdir(os.environ.get("HOME"))
                else:
                    self.send(f"cd: {msg[1]}: No such file or directory\n")
            case cmd if cmd in self.path_files.keys():
                os.system(f"{self.path_files[cmd]} {" ".join(msg[1:])}")
            case _:
                self.send(f"{msg[0]}: command not found\n")
        self.main()
        

if __name__ == "__main__":
    shell_instance = Shell()
    shell_instance.main()
