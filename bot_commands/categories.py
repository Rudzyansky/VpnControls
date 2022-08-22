from enum import IntFlag


class Categories(IntFlag):
    # User categories
    NO_ACCOUNTS = 1 << 0
    ONE_ACCOUNT = 1 << 1
    MANY_ACCOUNTS = 1 << 2
    # Administration categories
    NO_TOKENS = 1 << 3
    HAS_ACTUAL_TOKENS = 1 << 4
    CAN_ISSUE_TOKEN = 1 << 5
    HAS_TOKENS = 1 << 6
    HAS_SLAVES = 1 << 7
    GRANT = 1 << 8
    HAS_INVITED = 1 << 9
    # Common categories
    COMMON = 1 << 10


def decompose_categories(combined_categories: Categories) -> set[Categories]:
    def generator():
        for c in Categories:
            if c in combined_categories:
                yield c

    return {c for c in generator()}
