import os


def read_message(input_pipe: str) -> str:
    fd = os.open(input_pipe, os.O_RDONLY)
    message = f"PID {os.getpid()} received a message => {os.read(fd, 22).decode()}"
    os.close(fd)
    os.remove(named_pipe)

    return message


if __name__ == "__main__":
    named_pipe = "my_pipe"
    print(read_message(named_pipe))


"""
PID 35646 received a message => Hello from PID 35677
"""
