from enum import auto, IntFlag


# noinspection PyArgumentList
class Categories(IntFlag):
    # User categories
    NO_ACCOUNTS = auto()
    ONE_ACCOUNT = auto()
    MANY_ACCOUNTS = auto()
    # Administration categories
    NO_TOKENS = auto()
    HAS_ACTUAL_TOKENS = auto()
    CAN_ISSUE_TOKEN = auto()
    HAS_TOKENS = auto()
    HAS_SLAVES = auto()
    GRANT = auto()
    HAS_INVITED = auto()
    # Common categories
    COMMON = auto()


def decompose_categories(combined_categories: Categories) -> set[Categories]:
    def generator():
        for c in Categories:
            if c in combined_categories:
                yield c

    return {c for c in generator()}
