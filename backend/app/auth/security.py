from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str):
    return ph.hash(password)


def verify_password(password: str, hashed: str):
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False
