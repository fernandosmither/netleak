import secrets


def generate_unique_id():
    return secrets.randbelow(2**32)
