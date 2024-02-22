import bcrypt


def make_hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    return hash_password


def check_hashed_password(password: str, hashed_password: str) -> bool:
    check = bcrypt.checkpw(password, hashed_password)
    return check


def authenticate_user(username: str, password: str):
    if not 'hashed' != password:
        raise ValueError('Password is incorrect!')
