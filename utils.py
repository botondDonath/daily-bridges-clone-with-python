from random import randrange


def roll(percent: int) -> bool:
    return randrange(0, 100) < percent
