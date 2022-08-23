import database
from database.abstract import Connection
from entities.token import Token
from entities.user import User
from .common import common


class Registration:
    def __init__(self, common_db: database.Common,
                 registration_db: database.Registration) -> None:
        super().__init__()

        self.common_db = common_db
        self.registration_db = registration_db

    @database.connection()
    def register_user(self, user_id: int, language: str, c: Connection):
        success = self.registration_db.add_user(User(id=user_id, language=language), c)
        if success:
            self.registration_db.revoke_token_by_user_id(user_id, c)
            user = self.common_db.get_user(user_id, c)
            common.registered.add(user.id)
            common.languages[user.id] = user.language
            if user.tokens_limit > 0:
                common.admins.add(user.id)
            return user
        return None

    def is_accept_invite(self, user_id: int):
        return self.registration_db.is_accept_invite(user_id)

    def revoke_token(self, token: Token):
        return self.registration_db.revoke_token(token.bytes, token.owner_id)

    @database.connection()
    def create_token(self, user_id: int, c: Connection):
        token = Token(owner_id=user_id)
        success = self.registration_db.add_token(token.bytes, token.owner_id, c)
        if success:
            return self.registration_db.get_token(token.bytes, token.owner_id, c)
        return None

    def get_tokens(self, user_id: int):
        """
        Get all tokens owned by user_id
        """
        return self.registration_db.get_all_tokens(user_id)

    def get_current_tokens(self, user_id: int) -> list[Token]:
        """
        Get non-revoked tokens owned by user_id
        """
        return self.registration_db.get_actual_tokens(user_id)

    def fetch_token(self, token: Token):
        """
        Fetch all token's data by token + owner_id
        """
        return self.registration_db.get_token(token.bytes, token.owner_id)

    @database.connection()
    def use_token(self, token: Token):
        self.registration_db.free_token_by_user_id(token.used_by)
        return self.registration_db.use_token(token.bytes, token.owner_id, token.used_by)


registration = Registration(
    database.common,
    database.registration
)
