import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    sys.stdout.flush()

    # List of known commands
    cmds = []

    # Verify if use input is a command
    msg = input()
    if msg not in cmds:
        print(f"{msg}: command not found")


if __name__ == "__main__":
    main()
