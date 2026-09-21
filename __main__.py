import argparse

from .core import run

if __name__ == "__main__":
    sys_parser = argparse.ArgumentParser()

    sys_parser.add_argument("s", "shell", type=str)

    sys_args = sys_parser.parse_args()

    run(sys_args)
