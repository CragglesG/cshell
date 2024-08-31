import sys

def ask() -> None:
    # Signal for input
    send("$ ")

    msg = input()
    return msg.split(" ")


def send(msg: str) -> None:
    sys.stdout.write(msg)
    sys.stdout.flush()

def main():
    # Verify if use input is a command
    msg = ask()
    match msg[0]:
        case "exit":
            sys.exit(int(msg[1]))
        case "echo":
            send(" ".join(msg[1:]) + "\n")
        case _:
            send(f"{msg[0]}: command not found\n")
    main()

        
        


if __name__ == "__main__":
    main()
