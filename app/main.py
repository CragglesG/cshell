import sys
import os
import Levenshtein

class Shell:
    def __init__(self):
        # Set up the utility variables
        self.builtins = ["exit", "echo", "type", "pwd", "cd"]
        self.path = os.environ.get("PATH").split(":")
        self.path_files = {}

        # Fill up self.path_files with {name:path} entries
        for entry in self.path:
            if os.path.exists(entry):
                for content in os.scandir(entry):
                    if os.path.isfile(content.path):
                        self.path_files[content.name] = content.path
                    
    def ask(self) -> None:
        # Signal for input
        self.send("$ ")

        # Return a list of the command and arguments
        try:
            msg = input()
        except KeyboardInterrupt:
            self.send("\nWoah! Are you trying to kill me!? Next time, just type exit if you want me to go away.\n")
            os._exit(0)
        return msg.split(" ")

    def send(self, msg: str) -> None:
        # Print to the command line
        sys.stdout.write(msg)
        sys.stdout.flush()

    def main(self):
        # Ask for input and read it
        msg = self.ask()

        # Respond to the input appropriately
        match msg[0]:
            # Exit from the shell
            case "exit":
                if len(msg) == 1:
                    self.send("exit 0\n")
                    os._exit(0)
                else:
                    os._exit(int(msg[1]))

            # Echo the arguments
            case "echo":
                self.send(" ".join(msg[1:]) + "\n")

            # Check whether the first argument is a builtin, an executable, or not found
            case "type":
                if len(msg) != 1:
                    if msg[1] in self.builtins:
                        self.send(msg[1] + " is a shell builtin\n")
                    elif msg[1] in self.path_files.keys():
                        self.send(f"{msg[1]} is {self.path_files[msg[1]]}\n")
                    else:
                        self.send(f"type: {msg[1]}: not found\n")

            # Print the working directory
            case "pwd":
                self.send(os.getcwd() + "\n")

            # Change the working directory
            case "cd":
                if len(msg) == 1:
                    os.chdir(os.environ.get("HOME"))

                if os.path.isdir(msg[1]):
                    os.chdir(msg[1])
                elif msg[1] == "~":
                    os.chdir(os.environ.get("HOME"))
                elif os.path.isfile(msg[1]):
                    self.send(f"cd: {msg[1]}: Not a directory")
                else:
                    self.send(f"cd: {msg[1]}: No such file or directory\n")
            
            # Execute executables in path
            case cmd if cmd in self.path_files.keys():
                os.system(f"{self.path_files[cmd]} {" ".join(msg[1:])}")
            
            # Catch all other cases
            case _:
                self.send(f"{msg[0]}: command not found\n")
                distances = {'null':0}
                for cmd in [*self.builtins, *self.path_files]:
                    distances[cmd] = Levenshtein.jaro(msg[0], cmd, score_cutoff=0.8)
                if max(distances, key=distances.get) != 'null':
                    self.send(f"Did you mean {max(distances, key=distances.get)}?\n")
        try:        
            self.main()
        except Exception as err:
            self.send(f"Oops! It looks like an error occured! Here's some more details: {err}\n")
        finally:
            self.main()
        

if __name__ == "__main__":
    shell_instance = Shell()
    shell_instance.main()
