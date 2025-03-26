from db import Repository


def main():
    Repository.Common.remove_expired_tokens()
    Repository.Commands.recalculate_commands()


if __name__ == '__main__':
    main()
