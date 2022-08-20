import database
from entities.token import Token


class Users:
    def __init__(self, users_db: database.Users, tokens_db: database.Tokens) -> None:
        super().__init__()

        self.users_db = users_db
        self.tokens_db = tokens_db

        users = users_db.fetch_all()

        self.registered: list[int] = list(map(lambda u: u.id, users))
        self.admins: list[int] = list(map(lambda u: u.id, filter(lambda u: u.is_admin, users)))
        self.languages: dict[int, str] = dict(map(lambda u: (u.id, u.language), users))

    def language(self, user_id: int):
        return self.languages[user_id]

    def add_user(self, user_id: int):
        success = self.users_db.add_user(user_id)
        if success:
            user = self.users_db.fetch(user_id)
            self.registered.append(user.id)
            self.languages[user.id] = user.language
            if user.is_admin:
                self.admins.append(user.id)
        return success

    def is_accept_invite(self, user_id: int):
        return self.tokens_db.is_accept_invite(user_id)

    def revoke_token(self, token: Token):
        return self.tokens_db.revoke(token)

    def add_token(self, token: Token):
        return self.tokens_db.add(token)

    def get_tokens(self, user_id: int):
        """
        Get all tokens owned by user_id
        """
        return self.tokens_db.get_all(user_id)

    def fetch_token(self, token: Token):
        """
        Fetch all token's data by token + owner_id
        """
        return self.tokens_db.get(token)

    def use_token(self, token: Token):
        return self.tokens_db.use(token)
