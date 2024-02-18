import bcrypt


def make_hash_password(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    return hash_password


def check_hashed_password(password: str, hashed_password: str):
    check = bcrypt.checkpw(password, hashed_password)
    if not check:
        raise ValueError('Password is incorrect!')
    return check
