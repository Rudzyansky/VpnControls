import database
from database.abstract import Connection


@database.connection()
def main(c: Connection):
    database.commands.recalculate_commands(c=c)


if __name__ == '__main__':
    main()
