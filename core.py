import argparse
import shlex


def execute(parser, command):
    pass


def shell():
    while True:
        command = input("$ ").strip()

        if command in ["exit", "quit", "q"]:
            return

        execute(command)


def run(args):
    if args.shell:
        execute(shlex.split(args.shell))
        return

    shell()
