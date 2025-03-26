from db import Repository


def main():
    Repository.Commands.recalculate_commands()


if __name__ == '__main__':
    main()
