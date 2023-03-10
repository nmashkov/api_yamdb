import random


def create_confirmation_code():
    return str(random.randint(1000000000, 9999999999))
