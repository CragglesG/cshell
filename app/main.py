import sys

def ask():
    # Signal for input
    sys.stdout.write("$ ")
    sys.stdout.flush()

    msg = input()
    return msg

def main():
    # List of known commands
    cmds = []

    # Verify if use input is a command
    while True:
        msg = ask()
        if msg not in cmds:
            sys.stdout.write(f"{msg}: command not found\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
