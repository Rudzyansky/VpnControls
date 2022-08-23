import database


class Common:
    def __init__(self, common_db: database.Common,
                 registration_db: database.Registration) -> None:
        super().__init__()

        self.common_db = common_db
        self.registration_db = registration_db

        users = self.common_db.get_all_users()

        self.registered = {u.id for u in users}
        self.admins = {u.id for u in filter(lambda u: u.tokens_limit > 0, users)}
        self.languages: dict[int, str] = {u.id: u.language for u in users}

    def language(self, user_id: int):
        return self.languages[user_id]


common = Common(
    database.common,
    database.registration
)
