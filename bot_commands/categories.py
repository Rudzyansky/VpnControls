from enum import IntFlag


class Categories(IntFlag):
    # Accounts categories
    CAN_CREATE_ACCOUNT = 1 << 0
    ONE_ACCOUNT = 1 << 1
    MANY_ACCOUNTS = 1 << 2
    # Tokens categories
    HAS_ACTUAL_TOKENS = 1 << 4
    CAN_ISSUE_TOKEN = 1 << 5
    HAS_TOKENS = 1 << 6
    # Privileged categories
    HAS_USERS = 1 << 7
    # Common categories
    REGISTERED = 1 << 10


def decompose_categories(combined_categories: Categories) -> set[Categories]:
    def generator():
        for c in Categories:
            if c in combined_categories:
                yield c

    return {c for c in generator()}
