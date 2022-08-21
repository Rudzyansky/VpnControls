import database
from database import transaction
from database.abstract import Transaction
from entities.token import Token


class Users:
    def __init__(self, users_db: database.Users, tokens_db: database.Tokens) -> None:
        super().__init__()

        self.users_db = users_db
        self.tokens_db = tokens_db

        users = users_db.fetch_all()

        self.registered = [u.id for u in users]
        self.admins = [u.id for u in filter(lambda u: u.is_admin, users)]
        self.languages: dict[int, str] = {u.id: u.language for u in users}

    def language(self, user_id: int):
        return self.languages[user_id]

    @transaction
    def add_user(self, user_id: int, language: str, t: Transaction):
        success = self.users_db.add(user_id, language, t)
        if success:
            user = self.users_db.fetch(user_id, t)
            self.registered.append(user.id)
            self.languages[user.id] = user.language
            if user.is_admin:
                self.admins.append(user.id)
            return user
        return None

    def is_accept_invite(self, user_id: int):
        return self.tokens_db.is_accept_invite(user_id)

    def revoke_token(self, token: Token):
        return self.tokens_db.revoke(token)

    @transaction
    def create_token(self, user_id: int, t: Transaction):
        token = Token(owner_id=user_id)
        success = self.tokens_db.add(token, t)
        if success:
            return self.tokens_db.fetch(token, t)
        return None

    def get_tokens(self, user_id: int):
        """
        Get all tokens owned by user_id
        """
        return self.tokens_db.get_all(user_id)

    def get_current_tokens(self, user_id: int) -> list[Token]:
        """
        Get non-revoked tokens owned by user_id
        """
        return list(filter(lambda t: t.used_by is None or t.used_by != t.owner_id, self.get_tokens(user_id)))

    def fetch_token(self, token: Token):
        """
        Fetch all token's data by token + owner_id
        """
        return self.tokens_db.fetch(token)

    def use_token(self, token: Token):
        return self.tokens_db.use(token)
