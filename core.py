def execute():
    pass


def shell():
    while True:
        command = input("$ ").strip()

        if command in ["exit", "quit", "q"]:
            return

        execute(command)


def run(args):
    if args.shell:
        execute(args.shell)
        return

    shell()
