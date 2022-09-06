import database
from controls import controls
from database.abstract import Connection


@database.connection()
def main(c: Connection):
    for user_id in database.accounting.get_users(c=c):
        for account in database.accounting.get_accounts(user_id, c=c):
            position = controls.add_user(user_id, account.username, account.password)
            database.accounting.set_position(account.id, position, c=c)
    controls.update_hook()


if __name__ == '__main__':
    main()
