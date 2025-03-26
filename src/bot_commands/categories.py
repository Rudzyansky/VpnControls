from enum import IntFlag


class Categories(IntFlag):
    # Accounts categories
    CAN_CREATE_ACCOUNT = 1 << 1
    HAS_ACCOUNTS = 1 << 2
    # Tokens categories
    CAN_ISSUE_TOKEN = 1 << 3
    HAS_ACTUAL_TOKENS = 1 << 4
    HAS_TOKENS = 1 << 5
    # Privileged categories
    HAS_USERS = 1 << 6
    # Common categories
    REGISTERED = 1 << 0


def decompose_categories(combined_categories: Categories) -> set[Categories]:
    def generator():
        for c in Categories:
            if c in combined_categories:
                yield c

    return {c for c in generator()}
