import database


class Users:
    def __init__(self, users_db: database.Users, tokens_db: database.Tokens) -> None:
        super().__init__()

        self.users_db = users_db
        self.tokens_db = tokens_db

        users = users_db.fetch_all()

        self.registered: list[int] = list(map(lambda u: u.id, users))
        self.admins: list[int] = list(map(lambda u: u.id, filter(lambda u: u.is_admin, users)))
        self.languages: dict[int, str] = dict(map(lambda u: (u.id, u.language), users))

    def language(self, user_id):
        return self.languages[user_id]

    def add_user(self, user_id):
        success = self.users_db.add_user(user_id)
        if success:
            user = self.users_db.fetch(user_id)
            self.registered.append(user.id)
            self.languages[user.id] = user.language
            if user.is_admin:
                self.admins.append(user.id)
        return success

    def is_accept_invite(self, user_id):
        return self.tokens_db.is_accept_invite(user_id)
