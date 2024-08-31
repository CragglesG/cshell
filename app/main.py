import sys

def ask():
    # Signal for input
    sys.stdout.write("$ ")
    sys.stdout.flush()

    msg = input()
    return msg.split(" ")

def main():
    # Verify if use input is a command
    while True:
        msg = ask()
        if msg[0] == "exit":
            sys.exit(int(msg[1]))
        else:
            sys.stdout.write(f"{msg[0]}: command not found\n")
            sys.stdout.flush()
            continue
        


        
        


if __name__ == "__main__":
    main()
