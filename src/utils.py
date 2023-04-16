import os


def print_log(msg: str) -> None:
    if os.getenv("DEBUG", False):
        print(msg)
