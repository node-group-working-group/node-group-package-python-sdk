import argparse

from shell import execute, shell


def run(args):
    if args.shell:
        execute(args.shell)
        return

    shell()


if __name__ == "__main__":
    sys_parser = argparse.ArgumentParser(exit_on_error=False)
    sys_parser.add_argument("-s", "--shell", type=str)

    sys_args = sys_parser.parse_args()

    run(sys_args)
